from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import (
    ProjectViewSet, ProgressViewSet, ProgressImageViewSet, AuditLogViewSet,
    ContractorProfileViewSet, ContractorCertificateViewSet, ContractorSkillViewSet,
    MaterialViewSet, MaterialPaymentViewSet,
    IssueReportViewSet, IssueEvidenceViewSet,
    ContractorRatingViewSet, RatingEvidenceViewSet
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'progress', ProgressViewSet, basename='progress')
router.register(
    r'progress-images',
    ProgressImageViewSet,
    basename='progress-image'
)
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')

# ✅ Contractor Qualification System
router.register(r'contractor-profiles', ContractorProfileViewSet, basename='contractor-profile')
router.register(r'contractor-certificates', ContractorCertificateViewSet, basename='contractor-certificate')
router.register(r'contractor-skills', ContractorSkillViewSet, basename='contractor-skill')

# ✅ Material Transparency
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'material-payments', MaterialPaymentViewSet, basename='material-payment')

# ✅ Issue Reporting System
router.register(r'issues', IssueReportViewSet, basename='issue')
router.register(r'issue-evidence', IssueEvidenceViewSet, basename='issue-evidence')

# ✅ Proof-Based Ratings
router.register(r'contractor-ratings', ContractorRatingViewSet, basename='contractor-rating')
router.register(r'rating-evidence', RatingEvidenceViewSet, basename='rating-evidence')

urlpatterns = [
    path('', include(router.urls)),
]
