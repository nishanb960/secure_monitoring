from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone
import logging

logger = logging.getLogger('security')

class SecurityAuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.session['last_activity'] = timezone.now().timestamp()
            self.check_brute_force(request)
    
    def check_brute_force(self, request):
        ip = self.get_client_ip(request)
        key = f'bruteforce_{ip}'
        attempts = cache.get(key, 0)
        
        if attempts > 100:
            cache.set(f'blocked_{ip}', True, 3600)
            logger.warning(f"IP {ip} blocked due to excessive requests")
            return JsonResponse({'error': 'Too many requests'}, status=429)
        
        cache.set(key, attempts + 1, 60)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class AuditLogMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated and response.status_code >= 400:
            from logs.models import AuditLog
            AuditLog.objects.create(
                user=request.user,
                action=f"{request.method} {request.path}",
                status_code=response.status_code,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')