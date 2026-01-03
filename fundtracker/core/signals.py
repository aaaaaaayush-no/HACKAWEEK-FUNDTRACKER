from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    Project, Fund, Progress, AuditLog,
    ContractorProfile, ContractorCertificate, ContractorSkill,
    Material, MaterialPayment, IssueReport, ContractorRating
)


def create_audit(instance, action):
    AuditLog.objects.create(
        action=action,
        model_name=instance.__class__.__name__,
        object_id=instance.id,
        description=str(instance),
    )


@receiver(post_save, sender=Project)
@receiver(post_save, sender=Fund)
@receiver(post_save, sender=Progress)
@receiver(post_save, sender=ContractorProfile)
@receiver(post_save, sender=ContractorCertificate)
@receiver(post_save, sender=ContractorSkill)
@receiver(post_save, sender=Material)
@receiver(post_save, sender=MaterialPayment)
@receiver(post_save, sender=IssueReport)
@receiver(post_save, sender=ContractorRating)
def log_save(sender, instance, created, **kwargs):
    create_audit(instance, "CREATE" if created else "UPDATE")


@receiver(post_delete, sender=Project)
@receiver(post_delete, sender=Fund)
@receiver(post_delete, sender=Progress)
@receiver(post_delete, sender=ContractorProfile)
@receiver(post_delete, sender=ContractorCertificate)
@receiver(post_delete, sender=ContractorSkill)
@receiver(post_delete, sender=Material)
@receiver(post_delete, sender=MaterialPayment)
@receiver(post_delete, sender=IssueReport)
@receiver(post_delete, sender=ContractorRating)
def log_delete(sender, instance, **kwargs):
    create_audit(instance, "DELETE")
