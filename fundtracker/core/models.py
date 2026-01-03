from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    ministry = models.CharField(max_length=200)
    contractor = models.CharField(max_length=200)
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Fund(models.Model):
    project = models.ForeignKey(
        Project,
        related_name="funds",
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    released_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.amount}"


class Progress(models.Model):
    project = models.ForeignKey(
        Project,
        related_name="progress",
        on_delete=models.CASCADE
    )
    physical_progress = models.PositiveIntegerField()
    financial_progress = models.PositiveIntegerField()
    report_url = models.URLField(blank=True)
    date = models.DateField(auto_now_add=True)

    def clean(self):
        if self.physical_progress > 100 or self.financial_progress > 100:
            raise ValidationError("Progress cannot exceed 100%")

    def __str__(self):
        return f"{self.project.name} - {self.date}"


# ✅ OPTION E — AUDIT LOG
class AuditLog(models.Model):
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} {self.model_name} ({self.object_id})"

class ProgressImage(models.Model):
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='progress_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.progress}"

