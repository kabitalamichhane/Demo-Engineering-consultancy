from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ContactInquiry, QuoteRequest, WorkWithUsInquiry
from .notifications import send_submission_emails


@receiver(post_save, sender=ContactInquiry)
@receiver(post_save, sender=QuoteRequest)
@receiver(post_save, sender=WorkWithUsInquiry)
def notify_on_new_submission(sender, instance, created, **kwargs):
    """Fires for both website forms and API submissions, only when a NEW row is created."""
    if created:
        transaction.on_commit(lambda: send_submission_emails(instance))
