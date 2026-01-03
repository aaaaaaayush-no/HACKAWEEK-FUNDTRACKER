from rest_framework import serializers
from .models import Project, Fund, Progress, ProgressImage, UserProfile, AuditLog


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role']


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = "__all__"


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
        ]
        read_only_fields = ['submitted_by', 'reviewed_by', 'reviewed_at']


class ProjectSerializer(serializers.ModelSerializer):
    progress = ProgressSerializer(many=True, read_only=True)
    funds = FundSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'username', 'action', 'model_name', 'object_id', 'timestamp', 'description']

