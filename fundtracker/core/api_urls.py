from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import ProjectViewSet, ProgressViewSet, ProgressImageViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'progress', ProgressViewSet, basename='progress')
router.register(
    r'progress-images',
    ProgressImageViewSet,
    basename='progress-image'
)
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('', include(router.urls)),
]
