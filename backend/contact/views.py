"""
API views for contact messages.

Includes:
- Public contact form submission endpoint
- Admin endpoints for message management
- Health check endpoint
"""
import logging
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContactMessage
from .serializers import (
    ContactMessageCreateSerializer,
    ContactMessageListSerializer,
    ContactMessageUpdateSerializer,
)
from .services import create_contact_message
from .selectors import get_contact_messages
from .throttles import ContactRateThrottle

logger = logging.getLogger(__name__)


class ContactCreateView(APIView):
    """
    Public endpoint for contact form submissions.
    
    POST /api/contact/
    
    Accepts name, email, and message. Triggers async email notifications.
    Rate limited to prevent spam.
    """
    
    permission_classes = [AllowAny]
    throttle_classes = [ContactRateThrottle]
    
    def post(self, request):
        """Handle contact form submission."""
        serializer = ContactMessageCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check honeypot - if filled, pretend success but don't create
        if serializer.is_spam:
            logger.warning(
                f"Spam submission detected (honeypot filled) from IP: "
                f"{self._get_client_ip(request)}"
            )
            return Response(
                {'detail': 'Message received'},
                status=status.HTTP_201_CREATED
            )
        
        # Extract metadata from request
        ip_address = self._get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        
        # Create contact message via service
        create_contact_message(
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
            message=serializer.validated_data['message'],
            ip_address=ip_address,
            user_agent=user_agent,
        )
        
        return Response(
            {'detail': 'Message received'},
            status=status.HTTP_201_CREATED
        )
    
    def _get_client_ip(self, request) -> str:
        """Extract client IP from request, handling proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')


class ContactAdminViewSet(viewsets.ModelViewSet):
    """
    Admin endpoints for contact message management.
    
    GET /api/admin/contacts/ - List messages (with status filter)
    GET /api/admin/contacts/{id}/ - Retrieve single message
    PATCH /api/admin/contacts/{id}/ - Update status only
    
    Requires authentication and admin privileges.
    """
    
    permission_classes = [IsAdminUser]
    queryset = ContactMessage.objects.all()
    lookup_field = 'id'
    
    # Disable create and delete via API
    http_method_names = ['get', 'patch', 'head', 'options']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'partial_update':
            return ContactMessageUpdateSerializer
        return ContactMessageListSerializer
    
    def get_queryset(self):
        """Filter queryset by status if provided."""
        status_filter = self.request.query_params.get('status')
        return get_contact_messages(status=status_filter)
    
    def partial_update(self, request, *args, **kwargs):
        """Update contact message status."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return full representation after update
        return Response(
            ContactMessageListSerializer(instance).data
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Simple health check endpoint.
    
    GET /api/health/
    
    Returns basic health status for the API.
    Useful for load balancers and deployment health checks.
    """
    from django.db import connection
    
    health_status = {
        'status': 'healthy',
        'database': 'unknown',
        'celery': 'unchecked',  # Requires additional setup to check
    }
    
    # Check database connectivity
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        health_status['database'] = 'connected'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['database'] = f'error: {str(e)}'
    
    status_code = (
        status.HTTP_200_OK 
        if health_status['status'] == 'healthy' 
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )
    
    return Response(health_status, status=status_code)
