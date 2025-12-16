"""
Celery tasks for contact message email notifications.

Includes retry logic with exponential backoff for transient failures.
"""
import logging
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import ContactMessage

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=60,  # Initial retry delay in seconds
    retry_backoff_max=3600,  # Maximum retry delay (1 hour)
    retry_jitter=True,
    max_retries=5,
)
def send_user_confirmation_email(self, contact_id: str) -> None:
    """
    Send confirmation email to the user who submitted a contact form.
    
    Args:
        contact_id: UUID string of the contact message
    """
    logger.info(f"Starting user confirmation email task for contact {contact_id}")
    
    try:
        contact = ContactMessage.objects.get(id=contact_id)
    except ContactMessage.DoesNotExist:
        logger.warning(f"Contact message not found: {contact_id}")
        return  # Silently exit if contact doesn't exist
    
    subject = "Thanks for contacting Scalify Labs"
    
    body = f"""Hi {contact.name},

Thank you for reaching out to Scalify Labs!

We have received your message and will get back to you within 24-48 hours.

Here's a summary of what you sent:
---
{contact.message[:500]}{'...' if len(contact.message) > 500 else ''}
---

If you have any urgent matters, please feel free to follow up on this email.

Best regards,
The Scalify Labs Team
"""
    
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact.email],
            fail_silently=False,
        )
        logger.info(f"User confirmation email sent to {contact.email}")
    except Exception as e:
        logger.error(
            f"Failed to send user confirmation email for contact {contact_id}: {e}"
        )
        raise  # Re-raise for Celery retry


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=60,
    retry_backoff_max=3600,
    retry_jitter=True,
    max_retries=5,
)
def send_admin_notification_email(self, contact_id: str) -> None:
    """
    Send notification email to admin about new contact submission.
    
    Args:
        contact_id: UUID string of the contact message
    """
    logger.info(f"Starting admin notification email task for contact {contact_id}")
    
    try:
        contact = ContactMessage.objects.get(id=contact_id)
    except ContactMessage.DoesNotExist:
        logger.warning(f"Contact message not found: {contact_id}")
        return  # Silently exit if contact doesn't exist
    
    subject = "New Contact Message Received"
    
    body = f"""A new contact message has been received on the portfolio site.

SENDER INFORMATION
------------------
Name: {contact.name}
Email: {contact.email}
Submitted: {contact.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}
Source: {contact.source}

METADATA
--------
IP Address: {contact.ip_address or 'Not captured'}
User Agent: {contact.user_agent or 'Not captured'}

MESSAGE
-------
{contact.message}

---
View in admin: /admin/contact/contactmessage/{contact.id}/change/
"""
    
    admin_email = getattr(settings, 'ADMIN_CONTACT_EMAIL', settings.DEFAULT_FROM_EMAIL)
    
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False,
        )
        logger.info(f"Admin notification email sent for contact {contact_id}")
    except Exception as e:
        logger.error(
            f"Failed to send admin notification email for contact {contact_id}: {e}"
        )
        raise  # Re-raise for Celery retry
