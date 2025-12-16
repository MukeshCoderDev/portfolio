"""
Contact message business logic services.

Contains write operations and business logic for contact messages.
"""
import logging
from typing import Optional
from uuid import UUID

from .models import ContactMessage
from .tasks import send_user_confirmation_email, send_admin_notification_email

logger = logging.getLogger(__name__)


def create_contact_message(
    *,
    name: str,
    email: str,
    message: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    source: str = 'portfolio_site',
) -> ContactMessage:
    """
    Create a new contact message and dispatch email notifications.
    
    Args:
        name: Sender's name
        email: Sender's email address
        message: Message content
        ip_address: Optional IP address for spam tracking
        user_agent: Optional browser user agent
        source: Source of the contact (default: portfolio_site)
    
    Returns:
        The created ContactMessage instance
    """
    # Create the contact message
    contact = ContactMessage.objects.create(
        name=name,
        email=email,
        message=message,
        ip_address=ip_address,
        user_agent=user_agent,
        source=source,
    )
    
    # Log the creation
    logger.info(
        f"Contact message created: id={contact.id}, "
        f"email={email}, "
        f"message_preview={message[:50]}..."
    )
    
    # Dispatch async email tasks
    try:
        send_user_confirmation_email.delay(str(contact.id))
        send_admin_notification_email.delay(str(contact.id))
        logger.info(f"Email tasks dispatched for contact {contact.id}")
    except Exception as e:
        # Log but don't fail - emails are secondary to message storage
        logger.warning(
            f"Failed to dispatch email tasks for contact {contact.id}: {e}"
        )
    
    return contact


def update_contact_status(
    *,
    contact_id: UUID,
    status: str,
) -> Optional[ContactMessage]:
    """
    Update the status of a contact message.
    
    Args:
        contact_id: UUID of the contact message
        status: New status value
    
    Returns:
        The updated ContactMessage, or None if not found
    """
    try:
        contact = ContactMessage.objects.get(id=contact_id)
        old_status = contact.status
        contact.status = status
        contact.save(update_fields=['status', 'updated_at'])
        
        logger.info(
            f"Contact {contact_id} status updated: {old_status} -> {status}"
        )
        
        return contact
    except ContactMessage.DoesNotExist:
        logger.warning(f"Contact message not found: {contact_id}")
        return None
