"""
Contact message model.

Stores contact form submissions with metadata for tracking and admin workflow.
"""
import uuid
from django.db import models


class ContactMessage(models.Model):
    """
    Contact form submission from portfolio website.
    
    Includes sender information, message content, metadata for spam detection,
    and workflow status for admin processing.
    """
    
    # Status choices
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        REPLIED = 'REPLIED', 'Replied'
        ARCHIVED = 'ARCHIVED', 'Archived'
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identifier for this contact message'
    )
    
    # Sender information
    name = models.CharField(
        max_length=100,
        help_text='Name of the person contacting'
    )
    email = models.EmailField(
        db_index=True,
        help_text='Email address for reply'
    )
    message = models.TextField(
        max_length=2000,
        help_text='Message content'
    )
    
    # Metadata for spam detection and analytics
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text='IP address of the sender'
    )
    user_agent = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Browser user agent string'
    )
    
    # Workflow status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
        help_text='Current processing status'
    )
    
    # Source tracking for future campaigns
    source = models.CharField(
        max_length=50,
        default='portfolio_site',
        help_text='Source of the contact (e.g., portfolio_site, landing_page)'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text='When the message was submitted'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When the message was last updated'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['email', '-created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} <{self.email}> - {self.status} ({self.created_at.strftime('%Y-%m-%d')})"
