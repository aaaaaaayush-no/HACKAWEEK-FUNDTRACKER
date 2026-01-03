from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import (
    Project, Progress, ProgressImage, AuditLog,
    ContractorProfile, ContractorCertificate, ContractorSkill,
    Material, MaterialPayment, IssueReport, IssueEvidence,
    ContractorRating, RatingEvidence
)
from .serializers import (
    ProjectSerializer,
    ProgressSerializer,
    ProgressImageSerializer,
    AuditLogSerializer,
    ContractorProfileSerializer,
    ContractorCertificateSerializer,
    ContractorSkillSerializer,
    MaterialSerializer,
    MaterialPaymentSerializer,
    IssueReportSerializer,
    IssueEvidenceSerializer,
    ContractorRatingSerializer,
    RatingEvidenceSerializer
)
from .permissions import IsGovernment, IsAuditor, IsContractor


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    @action(detail=True, methods=['get'])
    def materials(self, request, pk=None):
        """
        ✅ Material Transparency - Get all materials for a project
        """
        project = self.get_object()
        materials = Material.objects.filter(project=project)
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def issues(self, request, pk=None):
        """
        ✅ Issue Reporting System - Get all issues for a project
        """
        project = self.get_object()
        issues = IssueReport.objects.filter(project=project)
        serializer = IssueReportSerializer(issues, many=True)
        return Response(serializer.data)


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    
    def create(self, request, *args, **kwargs):
        """
        ✅ Time-Based Reporting - Contractors can only submit reports after 5 PM
        """
        # Check time restriction for contractors
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            if request.user.profile.role == 'CONTRACTOR':
                current_time = timezone.localtime(timezone.now())
                if current_time.hour < 17:  # Before 5 PM (17:00)
                    return Response(
                        {
                            'error': 'Time restriction',
                            'message': f'Progress reports can only be submitted after 5:00 PM. '
                                       f'Current time: {current_time.strftime("%H:%M")}',
                            'current_time': current_time.strftime("%H:%M"),
                            'allowed_after': '17:00'
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                # ✅ Suspension System - Check if contractor is suspended
                if hasattr(request.user, 'contractor_profile'):
                    contractor_profile = request.user.contractor_profile
                    if contractor_profile.is_suspended:
                        return Response(
                            {
                                'error': 'Contractor suspended',
                                'message': f'Your account is suspended. Reason: {contractor_profile.suspension_reason}',
                                'suspended_at': contractor_profile.suspended_at
                            },
                            status=status.HTTP_403_FORBIDDEN
                        )
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # Automatically set submitted_by to current user
        serializer.save(submitted_by=self.request.user if self.request.user.is_authenticated else None)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pending(self, request):
        """Get all pending progress submissions"""
        pending_progress = Progress.objects.filter(status='PENDING')
        serializer = self.get_serializer(pending_progress, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsGovernment])
    def approve(self, request, pk=None):
        """Approve a progress submission (Government only)"""
        progress = self.get_object()
        progress.status = 'APPROVED'
        progress.reviewed_by = request.user
        progress.reviewed_at = timezone.now()
        progress.save()
        
        # Create audit log
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Progress',
            object_id=progress.id,
            description=f'Approved progress for {progress.project.name}'
        )
        
        serializer = self.get_serializer(progress)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsGovernment])
    def reject(self, request, pk=None):
        """Reject a progress submission (Government only)"""
        progress = self.get_object()
        progress.status = 'REJECTED'
        progress.reviewed_by = request.user
        progress.reviewed_at = timezone.now()
        progress.save()
        
        # Create audit log
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Progress',
            object_id=progress.id,
            description=f'Rejected progress for {progress.project.name}'
        )
        
        serializer = self.get_serializer(progress)
        return Response(serializer.data)


class ProgressImageViewSet(viewsets.ModelViewSet):
    queryset = ProgressImage.objects.all()
    serializer_class = ProgressImageSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        # Allow Government and Auditor roles to view audit logs
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()


# ✅ Contractor Qualification System ViewSets
class ContractorProfileViewSet(viewsets.ModelViewSet):
    queryset = ContractorProfile.objects.all()
    serializer_class = ContractorProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return own profile for contractors, all for government/auditors"""
        user = self.request.user
        if hasattr(user, 'profile'):
            if user.profile.role in ['GOVERNMENT', 'AUDITOR']:
                return ContractorProfile.objects.all()
            elif user.profile.role == 'CONTRACTOR':
                return ContractorProfile.objects.filter(user=user)
        return ContractorProfile.objects.none()
    
    @action(detail=True, methods=['get'])
    def check_eligibility(self, request, pk=None):
        """
        ✅ Contract Size Categories - Check contractor eligibility for contract sizes
        """
        contractor = self.get_object()
        eligibility = {
            'SMALL': contractor.check_contract_eligibility('SMALL'),
            'MEDIUM': contractor.check_contract_eligibility('MEDIUM'),
            'LARGE': contractor.check_contract_eligibility('LARGE'),
        }
        return Response({
            'contractor': contractor.user.username,
            'current_rating': str(contractor.rating),
            'is_suspended': contractor.is_suspended,
            'eligibility': {
                size: {'eligible': result[0], 'reason': result[1]}
                for size, result in eligibility.items()
            }
        })
    
    @action(detail=False, methods=['get'])
    def suspended(self, request):
        """
        ✅ Suspension System - Get all suspended contractors
        """
        suspended = ContractorProfile.objects.filter(is_suspended=True)
        serializer = self.get_serializer(suspended, many=True)
        return Response(serializer.data)


class ContractorCertificateViewSet(viewsets.ModelViewSet):
    queryset = ContractorCertificate.objects.all()
    serializer_class = ContractorCertificateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'contractor_profile'):
            return ContractorCertificate.objects.filter(contractor=user.contractor_profile)
        return ContractorCertificate.objects.none()
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'contractor_profile'):
            serializer.save(contractor=self.request.user.contractor_profile)


class ContractorSkillViewSet(viewsets.ModelViewSet):
    queryset = ContractorSkill.objects.all()
    serializer_class = ContractorSkillSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'contractor_profile'):
            return ContractorSkill.objects.filter(contractor=user.contractor_profile)
        return ContractorSkill.objects.none()
    
    def perform_create(self, serializer):
        if hasattr(self.request.user, 'contractor_profile'):
            serializer.save(contractor=self.request.user.contractor_profile)


# ✅ Material Transparency ViewSets
class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    
    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return Material.objects.filter(project_id=project_id)
        return Material.objects.all()
    
    @action(detail=True, methods=['post'], permission_classes=[IsGovernment])
    def verify(self, request, pk=None):
        """Government can verify material entries"""
        material = self.get_object()
        material.verified = True
        material.verified_by = request.user
        material.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='Material',
            object_id=material.id,
            description=f'Verified material: {material.name} for {material.project.name}'
        )
        
        serializer = self.get_serializer(material)
        return Response(serializer.data)


class MaterialPaymentViewSet(viewsets.ModelViewSet):
    queryset = MaterialPayment.objects.all()
    serializer_class = MaterialPaymentSerializer
    permission_classes = [IsAuthenticated]


# ✅ Issue Reporting System ViewSets
class IssueReportViewSet(viewsets.ModelViewSet):
    queryset = IssueReport.objects.all()
    serializer_class = IssueReportSerializer
    
    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user if self.request.user.is_authenticated else None)
    
    @action(detail=True, methods=['post'], permission_classes=[IsGovernment])
    def verify(self, request, pk=None):
        """
        ✅ Issue Reporting System - Government verifies issue reports
        """
        issue = self.get_object()
        issue.status = 'VERIFIED'
        issue.verified_by = request.user
        issue.verified_at = timezone.now()
        issue.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='IssueReport',
            object_id=issue.id,
            description=f'Verified issue: {issue.title}'
        )
        
        serializer = self.get_serializer(issue)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsGovernment])
    def forgive(self, request, pk=None):
        """
        ✅ Forgiveness System - Natural disasters can be forgiven
        """
        issue = self.get_object()
        
        if not issue.is_forgivable:
            return Response(
                {'error': 'This issue type cannot be forgiven'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        forgiveness_reason = request.data.get('reason', '')
        issue.is_forgiven = True
        issue.forgiveness_reason = forgiveness_reason
        issue.forgiven_by = request.user
        issue.forgiven_at = timezone.now()
        issue.status = 'FORGIVEN'
        issue.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='IssueReport',
            object_id=issue.id,
            description=f'Forgave issue: {issue.title}. Reason: {forgiveness_reason}'
        )
        
        serializer = self.get_serializer(issue)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsGovernment])
    def penalize(self, request, pk=None):
        """
        ✅ Issue Reporting System - Apply penalty to contractor
        """
        issue = self.get_object()
        
        if issue.is_forgiven:
            return Response(
                {'error': 'This issue has been forgiven'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        project = issue.project
        if project.contractor_profile:
            penalty = issue.apply_penalty(project.contractor_profile)
            
            AuditLog.objects.create(
                user=request.user,
                action='UPDATE',
                model_name='IssueReport',
                object_id=issue.id,
                description=f'Penalized contractor for issue: {issue.title}. Rating impact: -{penalty}'
            )
            
            serializer = self.get_serializer(issue)
            return Response({
                'issue': serializer.data,
                'penalty_applied': str(penalty),
                'new_contractor_rating': str(project.contractor_profile.rating)
            })
        
        return Response(
            {'error': 'No contractor profile linked to this project'},
            status=status.HTTP_400_BAD_REQUEST
        )


class IssueEvidenceViewSet(viewsets.ModelViewSet):
    queryset = IssueEvidence.objects.all()
    serializer_class = IssueEvidenceSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


# ✅ Proof-Based Ratings ViewSets
class ContractorRatingViewSet(viewsets.ModelViewSet):
    queryset = ContractorRating.objects.all()
    serializer_class = ContractorRatingSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(rated_by=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsGovernment])
    def verify(self, request, pk=None):
        """
        ✅ Proof-Based Ratings - Verify and apply rating
        """
        rating = self.get_object()
        
        # Check evidence requirement for negative ratings
        if rating.is_negative and rating.evidence_required and not rating.evidence_provided:
            return Response(
                {'error': 'Evidence is required for negative ratings but not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rating.is_verified = True
        rating.verified_by = request.user
        rating.verified_at = timezone.now()
        rating.save()
        
        # Apply rating to contractor
        rating.apply_to_contractor()
        
        AuditLog.objects.create(
            user=request.user,
            action='UPDATE',
            model_name='ContractorRating',
            object_id=rating.id,
            description=f'Verified and applied rating {rating.rating_value} for contractor {rating.contractor.user.username}'
        )
        
        serializer = self.get_serializer(rating)
        return Response({
            'rating': serializer.data,
            'new_contractor_rating': str(rating.contractor.rating)
        })


class RatingEvidenceViewSet(viewsets.ModelViewSet):
    queryset = RatingEvidence.objects.all()
    serializer_class = RatingEvidenceSerializer
    permission_classes = [IsAuthenticated]

