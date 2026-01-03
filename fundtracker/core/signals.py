from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Project, Fund, Progress, AuditLog


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
def log_save(sender, instance, created, **kwargs):
    create_audit(instance, "CREATE" if created else "UPDATE")


@receiver(post_delete, sender=Project)
@receiver(post_delete, sender=Fund)
@receiver(post_delete, sender=Progress)
def log_delete(sender, instance, **kwargs):
    create_audit(instance, "DELETE")
