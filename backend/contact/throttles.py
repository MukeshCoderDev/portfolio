"""
Custom throttling classes for contact API.

Provides rate limiting for the public contact endpoint to prevent spam.
"""
from rest_framework.throttling import SimpleRateThrottle


class ContactRateThrottle(SimpleRateThrottle):
    """
    Rate throttle for contact form submissions.
    
    Limits submissions per IP address to prevent spam.
    Uses the 'contact' rate from DRF settings (default: 10/hour).
    """
    
    scope = 'contact'
    
    def get_cache_key(self, request, view):
        """
        Generate cache key based on IP address.
        
        For anonymous users, we use IP-based throttling.
        Authenticated users are also throttled by IP to prevent abuse.
        """
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }
