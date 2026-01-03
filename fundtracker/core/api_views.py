from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project, Progress, ProgressImage, AuditLog
from .serializers import (
    ProjectSerializer,
    ProgressSerializer,
    ProgressImageSerializer,
    AuditLogSerializer
)
from .permissions import IsGovernment, IsAuditor


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    
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

