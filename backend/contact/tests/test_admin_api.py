"""
Tests for admin contact API endpoints.

Covers:
- Authentication requirements
- List/retrieve/update operations
- Permission checks
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from contact.models import ContactMessage

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture
def regular_user(db):
    """Create a regular (non-admin) user."""
    return User.objects.create_user(
        username='regular',
        email='regular@example.com',
        password='regularpass123'
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def sample_contacts(db):
    """Create sample contact messages for testing."""
    contacts = []
    statuses = [
        ContactMessage.Status.NEW,
        ContactMessage.Status.IN_PROGRESS,
        ContactMessage.Status.REPLIED,
    ]
    
    for i, contact_status in enumerate(statuses):
        contact = ContactMessage.objects.create(
            name=f'Contact {i}',
            email=f'contact{i}@example.com',
            message=f'Test message {i}',
            status=contact_status,
        )
        contacts.append(contact)
    
    return contacts


@pytest.mark.django_db
class TestAdminContactList:
    """Tests for GET /api/admin/contacts/ endpoint."""
    
    url = '/api/admin/contacts/'
    
    def test_list_requires_authentication(self, api_client):
        """Test that unauthenticated requests are rejected."""
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_list_requires_admin(self, api_client, regular_user):
        """Test that non-admin users are rejected."""
        api_client.force_authenticate(user=regular_user)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_list_success(self, api_client, admin_user, sample_contacts):
        """Test successful list retrieval by admin."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
    
    def test_list_filter_by_status(self, api_client, admin_user, sample_contacts):
        """Test filtering contacts by status."""
        api_client.force_authenticate(user=admin_user)
        
        response = api_client.get(self.url, {'status': 'NEW'})
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['status'] == 'NEW'
    
    def test_list_ordered_by_created_at(self, api_client, admin_user, sample_contacts):
        """Test that contacts are ordered by created_at descending."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)
        
        assert response.status_code == status.HTTP_200_OK
        results = response.data['results']
        
        # Most recent should be first
        for i in range(len(results) - 1):
            assert results[i]['created_at'] >= results[i + 1]['created_at']


@pytest.mark.django_db
class TestAdminContactRetrieve:
    """Tests for GET /api/admin/contacts/{id}/ endpoint."""
    
    def test_retrieve_requires_authentication(self, api_client, sample_contacts):
        """Test that unauthenticated requests are rejected."""
        contact = sample_contacts[0]
        response = api_client.get(f'/api/admin/contacts/{contact.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_retrieve_requires_admin(self, api_client, regular_user, sample_contacts):
        """Test that non-admin users are rejected."""
        api_client.force_authenticate(user=regular_user)
        contact = sample_contacts[0]
        response = api_client.get(f'/api/admin/contacts/{contact.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_retrieve_success(self, api_client, admin_user, sample_contacts):
        """Test successful single contact retrieval."""
        api_client.force_authenticate(user=admin_user)
        contact = sample_contacts[0]
        
        response = api_client.get(f'/api/admin/contacts/{contact.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(contact.id)
        assert response.data['name'] == contact.name
        assert response.data['email'] == contact.email
    
    def test_retrieve_not_found(self, api_client, admin_user):
        """Test 404 for non-existent contact."""
        api_client.force_authenticate(user=admin_user)
        
        response = api_client.get('/api/admin/contacts/00000000-0000-0000-0000-000000000000/')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestAdminContactUpdate:
    """Tests for PATCH /api/admin/contacts/{id}/ endpoint."""
    
    def test_update_requires_authentication(self, api_client, sample_contacts):
        """Test that unauthenticated requests are rejected."""
        contact = sample_contacts[0]
        response = api_client.patch(
            f'/api/admin/contacts/{contact.id}/',
            {'status': 'IN_PROGRESS'},
            format='json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_requires_admin(self, api_client, regular_user, sample_contacts):
        """Test that non-admin users are rejected."""
        api_client.force_authenticate(user=regular_user)
        contact = sample_contacts[0]
        
        response = api_client.patch(
            f'/api/admin/contacts/{contact.id}/',
            {'status': 'IN_PROGRESS'},
            format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_status_success(self, api_client, admin_user, sample_contacts):
        """Test successful status update."""
        api_client.force_authenticate(user=admin_user)
        contact = sample_contacts[0]
        assert contact.status == ContactMessage.Status.NEW
        
        response = api_client.patch(
            f'/api/admin/contacts/{contact.id}/',
            {'status': 'IN_PROGRESS'},
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'IN_PROGRESS'
        
        # Verify database update
        contact.refresh_from_db()
        assert contact.status == ContactMessage.Status.IN_PROGRESS
    
    def test_update_invalid_status(self, api_client, admin_user, sample_contacts):
        """Test validation error for invalid status."""
        api_client.force_authenticate(user=admin_user)
        contact = sample_contacts[0]
        
        response = api_client.patch(
            f'/api/admin/contacts/{contact.id}/',
            {'status': 'INVALID_STATUS'},
            format='json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_cannot_update_other_fields(self, api_client, admin_user, sample_contacts):
        """Test that other fields cannot be updated via API."""
        api_client.force_authenticate(user=admin_user)
        contact = sample_contacts[0]
        original_email = contact.email
        
        response = api_client.patch(
            f'/api/admin/contacts/{contact.id}/',
            {'status': 'REPLIED', 'email': 'hacked@example.com'},
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        
        # Email should not have changed
        contact.refresh_from_db()
        assert contact.email == original_email


@pytest.mark.django_db
class TestAdminContactMethodsRestricted:
    """Test that POST and DELETE are not allowed on admin endpoints."""
    
    url = '/api/admin/contacts/'
    
    def test_post_not_allowed(self, api_client, admin_user):
        """Test that POST is not allowed on admin endpoint."""
        api_client.force_authenticate(user=admin_user)
        
        response = api_client.post(
            self.url,
            {'name': 'Test', 'email': 'test@example.com', 'message': 'Test'},
            format='json'
        )
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_delete_not_allowed(self, api_client, admin_user, sample_contacts):
        """Test that DELETE is not allowed."""
        api_client.force_authenticate(user=admin_user)
        contact = sample_contacts[0]
        
        response = api_client.delete(f'/api/admin/contacts/{contact.id}/')
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
