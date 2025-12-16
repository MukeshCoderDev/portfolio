"""
Contact message serializers.

Includes serializers for public contact form submission and admin operations.
"""
import re
from rest_framework import serializers
from .models import ContactMessage


class ContactMessageCreateSerializer(serializers.Serializer):
    """
    Serializer for public contact form submission.
    
    Includes validation for spam protection:
    - Message length minimum
    - URL-only message detection
    - Honeypot field for bots
    """
    
    # Public fields
    name = serializers.CharField(
        max_length=100,
        required=True,
        help_text='Your name'
    )
    email = serializers.EmailField(
        required=True,
        help_text='Your email address'
    )
    message = serializers.CharField(
        max_length=2000,
        required=True,
        help_text='Your message'
    )
    
    # Honeypot field - should be empty, bots often fill this
    website = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        help_text='Leave this field empty'
    )
    
    def validate_name(self, value: str) -> str:
        """Strip whitespace from name."""
        return value.strip()
    
    def validate_email(self, value: str) -> str:
        """Normalize email to lowercase."""
        return value.lower().strip()
    
    def validate_message(self, value: str) -> str:
        """
        Validate message content for spam protection.
        
        - Strips whitespace
        - Rejects messages that are too short
        - Rejects messages that are only URLs
        """
        value = value.strip()
        
        # Minimum length check
        if len(value) < 10:
            raise serializers.ValidationError(
                'Message must be at least 10 characters long.'
            )
        
        # Check if message is only URLs
        url_pattern = r'https?://\S+'
        message_without_urls = re.sub(url_pattern, '', value).strip()
        
        if len(message_without_urls) < 10:
            raise serializers.ValidationError(
                'Please provide a meaningful message, not just links.'
            )
        
        return value
    
    def validate_website(self, value: str) -> str:
        """
        Honeypot validation.
        
        If this field is filled, it's likely a bot.
        We don't raise an error here - instead, we mark it as spam
        in the view and pretend success.
        """
        return value.strip() if value else ''
    
    @property
    def is_spam(self) -> bool:
        """Check if submission appears to be spam (honeypot filled)."""
        return bool(self.validated_data.get('website'))
    
    def create(self, validated_data: dict) -> ContactMessage:
        """Create a new contact message (excluding honeypot field)."""
        validated_data.pop('website', None)
        return ContactMessage.objects.create(**validated_data)


class ContactMessageListSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for admin contact message list.
    """
    
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = ContactMessage
        fields = [
            'id',
            'name',
            'email',
            'message',
            'status',
            'status_display',
            'source',
            'ip_address',
            'user_agent',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class ContactMessageUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for admin status updates.
    
    Only the status field can be modified.
    """
    
    class Meta:
        model = ContactMessage
        fields = ['status']
    
    def validate_status(self, value: str) -> str:
        """Validate status is a valid choice."""
        valid_statuses = [choice[0] for choice in ContactMessage.Status.choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            )
        return value
