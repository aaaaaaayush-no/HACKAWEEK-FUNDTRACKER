from rest_framework import viewsets
from .models import Project, Progress, ProgressImage
from .serializers import (
    ProjectSerializer,
    ProgressSerializer,
    ProgressImageSerializer
)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer


class ProgressImageViewSet(viewsets.ModelViewSet):
    queryset = ProgressImage.objects.all()
    serializer_class = ProgressImageSerializer
