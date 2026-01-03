from django.contrib import admin
from .models import Project, Fund, Progress
from .models import AuditLog



class FundInline(admin.TabularInline):
    model = Fund
    extra = 1


class ProgressInline(admin.TabularInline):
    model = Progress
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "ministry", "total_budget")
    inlines = [FundInline, ProgressInline]


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ("project", "amount", "released_at")


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ("project", "physical_progress", "financial_progress", "date")


from .models import AuditLog


from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "model_name", "object_id")
    list_filter = ("action", "model_name")
    search_fields = ("user__username", "model_name", "object_id")

