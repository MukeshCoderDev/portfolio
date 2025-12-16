"""
Tests for Celery email tasks.

Covers:
- Task execution with mocked email
- Handling of missing contacts
- Retry behavior
"""
import pytest
from unittest.mock import patch, MagicMock

from contact.models import ContactMessage
from contact.tasks import send_user_confirmation_email, send_admin_notification_email


@pytest.fixture
def sample_contact(db):
    """Create a sample contact message for testing."""
    return ContactMessage.objects.create(
        name='Test User',
        email='test@example.com',
        message='This is a test message for email task testing.',
        ip_address='192.168.1.1',
        user_agent='Test Browser/1.0',
    )


@pytest.mark.django_db
class TestUserConfirmationEmail:
    """Tests for send_user_confirmation_email task."""
    
    @patch('contact.tasks.send_mail')
    def test_sends_email_successfully(self, mock_send_mail, sample_contact):
        """Test that email is sent with correct parameters."""
        send_user_confirmation_email(str(sample_contact.id))
        
        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args
        
        # Check subject
        assert 'Thanks for contacting' in call_kwargs[1]['subject']
        
        # Check recipient
        assert sample_contact.email in call_kwargs[1]['recipient_list']
        
        # Check body contains user name
        assert sample_contact.name in call_kwargs[1]['message']
    
    @patch('contact.tasks.send_mail')
    def test_handles_missing_contact(self, mock_send_mail):
        """Test that task handles non-existent contact gracefully."""
        # Should not raise an exception
        send_user_confirmation_email('00000000-0000-0000-0000-000000000000')
        
        # Email should not be sent
        mock_send_mail.assert_not_called()
    
    @patch('contact.tasks.send_mail')
    def test_retries_on_email_failure(self, mock_send_mail, sample_contact):
        """Test that task raises exception on email failure for retry."""
        mock_send_mail.side_effect = Exception('SMTP Error')
        
        with pytest.raises(Exception, match='SMTP Error'):
            send_user_confirmation_email(str(sample_contact.id))


@pytest.mark.django_db
class TestAdminNotificationEmail:
    """Tests for send_admin_notification_email task."""
    
    @patch('contact.tasks.send_mail')
    def test_sends_email_successfully(self, mock_send_mail, sample_contact):
        """Test that admin notification is sent with correct parameters."""
        send_admin_notification_email(str(sample_contact.id))
        
        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args
        
        # Check subject
        assert 'New Contact Message' in call_kwargs[1]['subject']
        
        # Check body contains contact info
        body = call_kwargs[1]['message']
        assert sample_contact.name in body
        assert sample_contact.email in body
        assert sample_contact.message in body
        assert sample_contact.ip_address in body
    
    @patch('contact.tasks.send_mail')
    def test_handles_missing_contact(self, mock_send_mail):
        """Test that task handles non-existent contact gracefully."""
        send_admin_notification_email('00000000-0000-0000-0000-000000000000')
        
        mock_send_mail.assert_not_called()
    
    @patch('contact.tasks.send_mail')
    def test_handles_missing_metadata(self, mock_send_mail, db):
        """Test email still sends when metadata is None."""
        contact = ContactMessage.objects.create(
            name='No Metadata User',
            email='nometadata@example.com',
            message='Message without IP or user agent',
            ip_address=None,
            user_agent=None,
        )
        
        send_admin_notification_email(str(contact.id))
        
        mock_send_mail.assert_called_once()
        body = mock_send_mail.call_args[1]['message']
        assert 'Not captured' in body
