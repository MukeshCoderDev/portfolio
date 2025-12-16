"""
Tests for public contact API endpoint.

Covers:
- Successful contact creation
- Validation errors
- Honeypot spam detection
- Rate limiting
"""
import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from contact.models import ContactMessage


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def valid_contact_data():
    """Return valid contact form data."""
    return {
        'name': 'John Doe',
        'email': 'john@example.com',
        'message': 'Hello, I am interested in your services. Please contact me.',
    }


@pytest.mark.django_db
class TestContactCreate:
    """Tests for POST /api/contact/ endpoint."""
    
    url = '/api/contact/'
    
    def test_create_contact_success(self, api_client, valid_contact_data):
        """Test successful contact creation."""
        with patch('contact.services.send_user_confirmation_email.delay'):
            with patch('contact.services.send_admin_notification_email.delay'):
                response = api_client.post(
                    self.url,
                    valid_contact_data,
                    format='json'
                )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'detail': 'Message received'}
        
        # Verify database record created
        assert ContactMessage.objects.count() == 1
        contact = ContactMessage.objects.first()
        assert contact.name == valid_contact_data['name']
        assert contact.email == valid_contact_data['email']
        assert contact.message == valid_contact_data['message']
        assert contact.status == ContactMessage.Status.NEW
    
    def test_create_contact_captures_metadata(self, api_client, valid_contact_data):
        """Test that IP address and user agent are captured."""
        with patch('contact.services.send_user_confirmation_email.delay'):
            with patch('contact.services.send_admin_notification_email.delay'):
                response = api_client.post(
                    self.url,
                    valid_contact_data,
                    format='json',
                    HTTP_USER_AGENT='Mozilla/5.0 Test Browser',
                    REMOTE_ADDR='192.168.1.100',
                )
        
        assert response.status_code == status.HTTP_201_CREATED
        
        contact = ContactMessage.objects.first()
        assert contact.user_agent == 'Mozilla/5.0 Test Browser'
        assert contact.ip_address == '192.168.1.100'
    
    def test_create_contact_missing_name(self, api_client):
        """Test validation error when name is missing."""
        response = api_client.post(
            self.url,
            {'email': 'test@example.com', 'message': 'Hello, this is a test message'},
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data
    
    def test_create_contact_missing_email(self, api_client):
        """Test validation error when email is missing."""
        response = api_client.post(
            self.url,
            {'name': 'Test User', 'message': 'Hello, this is a test message'},
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
    
    def test_create_contact_invalid_email(self, api_client):
        """Test validation error for invalid email format."""
        response = api_client.post(
            self.url,
            {
                'name': 'Test User',
                'email': 'not-an-email',
                'message': 'Hello, this is a test message'
            },
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
    
    def test_create_contact_message_too_short(self, api_client):
        """Test validation error when message is too short."""
        response = api_client.post(
            self.url,
            {
                'name': 'Test User',
                'email': 'test@example.com',
                'message': 'Short'
            },
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'message' in response.data
    
    def test_create_contact_message_only_urls(self, api_client):
        """Test validation error when message contains only URLs."""
        response = api_client.post(
            self.url,
            {
                'name': 'Test User',
                'email': 'test@example.com',
                'message': 'https://spam.com https://another-spam.com'
            },
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'message' in response.data
    
    def test_create_contact_honeypot_filled(self, api_client, valid_contact_data):
        """Test honeypot detection - returns success but doesn't create record."""
        data = {**valid_contact_data, 'website': 'http://spam.com'}
        
        response = api_client.post(self.url, data, format='json')
        
        # Should return success to fool bots
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == {'detail': 'Message received'}
        
        # But no record should be created
        assert ContactMessage.objects.count() == 0
    
    def test_create_contact_normalizes_email(self, api_client):
        """Test that email is normalized to lowercase."""
        data = {
            'name': 'Test User',
            'email': 'TEST@EXAMPLE.COM',
            'message': 'Hello, this is a test message for normalization check'
        }
        
        with patch('contact.services.send_user_confirmation_email.delay'):
            with patch('contact.services.send_admin_notification_email.delay'):
                response = api_client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        contact = ContactMessage.objects.first()
        assert contact.email == 'test@example.com'
    
    def test_create_contact_trims_whitespace(self, api_client):
        """Test that whitespace is trimmed from inputs."""
        data = {
            'name': '  Test User  ',
            'email': '  test@example.com  ',
            'message': '  Hello, this is a test message with whitespace  '
        }
        
        with patch('contact.services.send_user_confirmation_email.delay'):
            with patch('contact.services.send_admin_notification_email.delay'):
                response = api_client.post(self.url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        contact = ContactMessage.objects.first()
        assert contact.name == 'Test User'
        assert contact.message.startswith('Hello')


@pytest.mark.django_db
class TestContactRateLimit:
    """Tests for contact endpoint rate limiting."""
    
    url = '/api/contact/'
    
    def test_rate_limit_exceeded(self, api_client, valid_contact_data, settings):
        """Test rate limiting after too many requests."""
        from django.core.cache import cache
        
        # Clear cache to ensure fresh rate limit state
        cache.clear()
        
        # Set a low rate limit for testing
        settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['contact'] = '2/hour'
        
        with patch('contact.services.send_user_confirmation_email.delay'):
            with patch('contact.services.send_admin_notification_email.delay'):
                # First two requests should succeed
                for i in range(2):
                    response = api_client.post(
                        self.url,
                        {**valid_contact_data, 'message': f'Message number {i} with enough characters'},
                        format='json'
                    )
                    assert response.status_code == status.HTTP_201_CREATED, f"Request {i} failed"
                
                # Third request should be throttled
                response = api_client.post(
                    self.url,
                    valid_contact_data,
                    format='json'
                )
                assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
