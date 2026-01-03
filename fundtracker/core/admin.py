from django.contrib import admin
from .models import (
    Project, Fund, Progress, AuditLog, UserProfile,
    ContractorProfile, ContractorCertificate, ContractorSkill,
    Material, MaterialPayment, ProgressImage,
    IssueReport, IssueEvidence, ContractorRating, RatingEvidence
)


# Inline classes
class FundInline(admin.TabularInline):
    model = Fund
    extra = 1


class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 1


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1


class IssueInline(admin.TabularInline):
    model = IssueReport
    extra = 0


class CertificateInline(admin.TabularInline):
    model = ContractorCertificate
    extra = 1


class SkillInline(admin.TabularInline):
    model = ContractorSkill
    extra = 1


class IssueEvidenceInline(admin.TabularInline):
    model = IssueEvidence
    extra = 1


class RatingEvidenceInline(admin.TabularInline):
    model = RatingEvidence
    extra = 1


class MaterialPaymentInline(admin.TabularInline):
    model = MaterialPayment
    extra = 1


# Model Admin classes
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "nepal_nid", "nid_verified")
    list_filter = ("role", "nid_verified")
    search_fields = ("user__username", "nepal_nid")


@admin.register(ContractorProfile)
class ContractorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "rating", "is_suspended", "skill_level", "years_of_experience", "test_passed")
    list_filter = ("is_suspended", "skill_level", "test_passed")
    search_fields = ("user__username",)
    inlines = [CertificateInline, SkillInline]
    readonly_fields = ("ai_rating", "ai_rating_updated_at", "ai_risk_score")
    fieldsets = (
        (None, {
            'fields': ('user', 'rating', 'total_projects_completed', 'total_projects_failed')
        }),
        ('Suspension Status', {
            'fields': ('is_suspended', 'suspension_reason', 'suspended_at'),
            'classes': ('collapse',)
        }),
        ('Qualifications', {
            'fields': ('years_of_experience', 'skill_level', 'qualification_test_score', 'test_passed', 'test_taken_at')
        }),
        ('AI Integration (Read-only)', {
            'fields': ('ai_rating', 'ai_rating_updated_at', 'ai_risk_score'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContractorCertificate)
class ContractorCertificateAdmin(admin.ModelAdmin):
    list_display = ("name", "contractor", "issuing_authority", "issue_date", "expiry_date", "verified")
    list_filter = ("verified", "issuing_authority")
    search_fields = ("name", "contractor__user__username")


@admin.register(ContractorSkill)
class ContractorSkillAdmin(admin.ModelAdmin):
    list_display = ("skill_name", "contractor", "proficiency_level", "years_of_practice", "verified")
    list_filter = ("verified", "proficiency_level")
    search_fields = ("skill_name", "contractor__user__username")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "ministry", "total_budget", "contract_size", "status", "start_date", "end_date")
    list_filter = ("contract_size", "status", "ministry")
    search_fields = ("name", "contractor", "location")
    inlines = [FundInline, ProgressInline, MaterialInline, IssueInline]
    readonly_fields = ("contract_size", "min_contractor_rating")
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'ministry', 'contractor', 'contractor_profile', 'total_budget')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'completion_date', 'status')
        }),
        ('Contract Details (Auto-calculated)', {
            'fields': ('contract_size', 'min_contractor_rating'),
        }),
        ('Work Longevity', {
            'fields': ('expected_lifespan_years', 'actual_lifespan_years', 'warranty_period_years'),
        }),
        ('Blockchain Integration', {
            'fields': ('blockchain_tx_hash', 'blockchain_contract_address'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ("project", "amount", "released_at", "blockchain_confirmed")
    list_filter = ("blockchain_confirmed",)
    search_fields = ("project__name",)


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("project", "physical_progress", "financial_progress", "date", "status", "submitted_by")
    list_filter = ("status", "date")
    search_fields = ("project__name",)


@admin.register(ProgressImage)
class ProgressImageAdmin(admin.ModelAdmin):
    list_display = ("progress", "uploaded_at")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "unit", "planned_quantity", "unit_price", "total_planned_cost", "verified")
    list_filter = ("verified", "unit")
    search_fields = ("name", "project__name", "supplier_name")
    inlines = [MaterialPaymentInline]
    readonly_fields = ("total_planned_cost", "total_actual_cost")


@admin.register(MaterialPayment)
class MaterialPaymentAdmin(admin.ModelAdmin):
    list_display = ("material", "amount", "payment_date", "status", "payment_reference")
    list_filter = ("status",)
    search_fields = ("payment_reference", "material__name")


@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "issue_type", "severity", "status", "is_forgivable", "is_forgiven")
    list_filter = ("issue_type", "severity", "status", "is_forgiven")
    search_fields = ("title", "project__name")
    inlines = [IssueEvidenceInline]
    fieldsets = (
        (None, {
            'fields': ('project', 'title', 'description', 'issue_type', 'severity', 'status')
        }),
        ('Forgiveness System', {
            'fields': ('is_forgivable', 'is_forgiven', 'forgiveness_reason', 'forgiven_by', 'forgiven_at'),
        }),
        ('Verification', {
            'fields': ('reported_by', 'reported_at', 'verified_by', 'verified_at'),
        }),
        ('Resolution', {
            'fields': ('rating_impact', 'resolution_notes', 'resolved_at'),
        }),
    )


@admin.register(IssueEvidence)
class IssueEvidenceAdmin(admin.ModelAdmin):
    list_display = ("issue", "evidence_type", "uploaded_by", "uploaded_at")
    list_filter = ("evidence_type",)


@admin.register(ContractorRating)
class ContractorRatingAdmin(admin.ModelAdmin):
    list_display = ("contractor", "project", "rating_value", "rated_by", "is_negative", "evidence_required", "evidence_provided", "is_verified")
    list_filter = ("is_negative", "is_verified", "rating_value")
    search_fields = ("contractor__user__username", "project__name")
    inlines = [RatingEvidenceInline]


@admin.register(RatingEvidence)
class RatingEvidenceAdmin(admin.ModelAdmin):
    list_display = ("rating", "evidence_type", "uploaded_at")
    list_filter = ("evidence_type",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "model_name", "object_id")
    list_filter = ("action", "model_name")
    search_fields = ("user__username", "model_name", "object_id")

