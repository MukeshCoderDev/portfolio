"""
Contact message query selectors.

Contains read operations and query helpers for contact messages.
"""
from typing import Optional
from uuid import UUID

from django.db.models import QuerySet

from .models import ContactMessage


def get_contact_messages(
    *,
    status: Optional[str] = None,
) -> QuerySet[ContactMessage]:
    """
    Get contact messages with optional filtering.
    
    Args:
        status: Optional status filter (NEW, IN_PROGRESS, REPLIED, ARCHIVED)
    
    Returns:
        QuerySet of ContactMessage instances
    """
    queryset = ContactMessage.objects.all()
    
    if status:
        queryset = queryset.filter(status=status)
    
    return queryset


def get_contact_message_by_id(
    *,
    contact_id: UUID,
) -> Optional[ContactMessage]:
    """
    Get a single contact message by ID.
    
    Args:
        contact_id: UUID of the contact message
    
    Returns:
        ContactMessage instance or None if not found
    """
    try:
        return ContactMessage.objects.get(id=contact_id)
    except ContactMessage.DoesNotExist:
        return None


def get_contact_messages_by_email(
    *,
    email: str,
) -> QuerySet[ContactMessage]:
    """
    Get all contact messages from a specific email address.
    
    Useful for detecting repeat contacts or potential spam.
    
    Args:
        email: Email address to filter by
    
    Returns:
        QuerySet of ContactMessage instances
    """
    return ContactMessage.objects.filter(email__iexact=email)


def get_recent_contact_count_by_ip(
    *,
    ip_address: str,
    hours: int = 24,
) -> int:
    """
    Count recent contact messages from an IP address.
    
    Useful for rate limiting and spam detection.
    
    Args:
        ip_address: IP address to check
        hours: Time window in hours (default: 24)
    
    Returns:
        Count of messages from this IP in the time window
    """
    from django.utils import timezone
    from datetime import timedelta
    
    cutoff = timezone.now() - timedelta(hours=hours)
    return ContactMessage.objects.filter(
        ip_address=ip_address,
        created_at__gte=cutoff,
    ).count()
