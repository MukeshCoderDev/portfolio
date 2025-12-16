"""
URL configuration for contact API.

Routes:
- /api/contact/ - Public contact form endpoint
- /api/admin/contacts/ - Admin management endpoints
- /api/health/ - Health check
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ContactCreateView, ContactAdminViewSet, health_check

# Router for admin viewset
router = DefaultRouter()
router.register(r'admin/contacts', ContactAdminViewSet, basename='admin-contacts')

urlpatterns = [
    # Public contact endpoint
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
    
    # Health check
    path('health/', health_check, name='health-check'),
    
    # Admin endpoints via router
    path('', include(router.urls)),
]
