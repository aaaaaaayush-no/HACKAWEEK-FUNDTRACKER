from rest_framework import serializers
from .models import (
    Project, Fund, Progress, ProgressImage, UserProfile, AuditLog,
    ContractorProfile, ContractorCertificate, ContractorSkill,
    Material, MaterialPayment, IssueReport, IssueEvidence,
    ContractorRating, RatingEvidence
)


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role', 'nepal_nid', 'nid_verified']
        read_only_fields = ['nid_verified']


# ✅ Contractor Qualification System Serializers
class ContractorCertificateSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = ContractorCertificate
        fields = '__all__'
        read_only_fields = ['verified']


class ContractorSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorSkill
        fields = '__all__'
        read_only_fields = ['verified']


class ContractorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    certificates = ContractorCertificateSerializer(many=True, read_only=True)
    skills = ContractorSkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = ContractorProfile
        fields = [
            'id', 'username', 'rating', 'total_projects_completed', 
            'total_projects_failed', 'is_suspended', 'suspension_reason',
            'suspended_at', 'years_of_experience', 'skill_level',
            'qualification_test_score', 'test_passed', 'test_taken_at',
            'ai_rating', 'ai_rating_updated_at', 'ai_risk_score',
            'certificates', 'skills', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'rating', 'is_suspended', 'suspension_reason', 'suspended_at',
            'ai_rating', 'ai_rating_updated_at', 'ai_risk_score',
            'test_passed', 'test_taken_at'
        ]


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = "__all__"


# ✅ Material Transparency Serializers
class MaterialPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialPayment
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    payments = MaterialPaymentSerializer(many=True, read_only=True)
    cost_variance = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    
    class Meta:
        model = Material
        fields = [
            'id', 'project', 'name', 'description', 'unit',
            'planned_quantity', 'actual_quantity', 'unit_price',
            'total_planned_cost', 'total_actual_cost', 'cost_variance',
            'supplier_name', 'supplier_contact', 'quality_grade',
            'verified', 'verified_by', 'payments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['total_planned_cost', 'total_actual_cost', 'verified', 'verified_by']


class ProgressImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressImage
        fields = "__all__"


class ProgressSerializer(serializers.ModelSerializer):
    images = ProgressImageSerializer(many=True, read_only=True)
    submitted_by_username = serializers.CharField(source='submitted_by.username', read_only=True)
    reviewed_by_username = serializers.CharField(source='reviewed_by.username', read_only=True)

    class Meta:
        model = Progress
        fields = [
            "id",
            "project",
            "physical_progress",
            "financial_progress",
            "report_url",
            "date",
            "images",
            "status",
            "submitted_by",
            "submitted_by_username",
            "reviewed_by",
            "reviewed_by_username",
            "reviewed_at",
            "submitted_at",
            "blockchain_tx_hash",
        ]
        read_only_fields = ['submitted_by', 'reviewed_by', 'reviewed_at', 'submitted_at', 'blockchain_tx_hash']


class ProjectSerializer(serializers.ModelSerializer):
    progress = ProgressSerializer(many=True, read_only=True)
    funds = FundSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    contractor_profile_detail = ContractorProfileSerializer(source='contractor_profile', read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ['contract_size', 'min_contractor_rating']


class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'username', 'action', 'model_name', 'object_id', 'timestamp', 'description']


# ✅ Issue Reporting System Serializers
class IssueEvidenceSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = IssueEvidence
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'uploaded_at']


class IssueReportSerializer(serializers.ModelSerializer):
    evidence = IssueEvidenceSerializer(many=True, read_only=True)
    reported_by_username = serializers.CharField(source='reported_by.username', read_only=True)
    verified_by_username = serializers.CharField(source='verified_by.username', read_only=True)
    forgiven_by_username = serializers.CharField(source='forgiven_by.username', read_only=True)
    
    class Meta:
        model = IssueReport
        fields = [
            'id', 'project', 'title', 'description', 'issue_type',
            'severity', 'status', 'is_forgivable', 'forgiveness_reason',
            'is_forgiven', 'forgiven_by', 'forgiven_by_username', 'forgiven_at',
            'reported_by', 'reported_by_username', 'reported_at',
            'verified_by', 'verified_by_username', 'verified_at',
            'rating_impact', 'resolution_notes', 'resolved_at',
            'evidence', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'is_forgivable', 'is_forgiven', 'forgiven_by', 'forgiven_at',
            'reported_by', 'reported_at', 'verified_by', 'verified_at',
            'rating_impact', 'resolved_at', 'status'
        ]


# ✅ Proof-Based Ratings Serializers
class RatingEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingEvidence
        fields = '__all__'


class ContractorRatingSerializer(serializers.ModelSerializer):
    evidence = RatingEvidenceSerializer(many=True, read_only=True)
    rated_by_username = serializers.CharField(source='rated_by.username', read_only=True)
    contractor_username = serializers.CharField(source='contractor.user.username', read_only=True)
    verified_by_username = serializers.CharField(source='verified_by.username', read_only=True)
    
    class Meta:
        model = ContractorRating
        fields = [
            'id', 'contractor', 'contractor_username', 'project',
            'rated_by', 'rated_by_username', 'rating_value', 'comment',
            'is_negative', 'evidence_required', 'evidence_provided',
            'is_verified', 'verified_by', 'verified_by_username', 'verified_at',
            'evidence', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'rated_by', 'is_negative', 'evidence_required', 'evidence_provided',
            'is_verified', 'verified_by', 'verified_at'
        ]
    
    def validate(self, data):
        """
        ✅ Proof-Based Ratings - Check if evidence is provided for negative ratings
        """
        rating_value = data.get('rating_value')
        if rating_value and rating_value <= 2:
            # Check if evidence files are being uploaded
            request = self.context.get('request')
            if request and not request.FILES.getlist('evidence'):
                raise serializers.ValidationError({
                    'evidence': 'Photo/video evidence is required for ratings of 2 or below.'
                })
        return data

