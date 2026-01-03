from rest_framework import serializers
from .models import Project, Fund, Progress, ProgressImage


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
        ]


class ProjectSerializer(serializers.ModelSerializer):
    progress = ProgressSerializer(many=True, read_only=True)
    funds = FundSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
