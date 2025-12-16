"""
Django admin configuration for Contact app.

Provides a clean interface for managing contact messages with filtering,
search, and read-only metadata fields.
"""
from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for ContactMessage model."""
    
    list_display = ('name', 'email', 'status', 'source', 'created_at')
    list_filter = ('status', 'source', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('id', 'ip_address', 'user_agent', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'message')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'source')
        }),
        ('Metadata', {
            'fields': ('id', 'ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        """Disable adding messages from admin (should come from API)."""
        return False
