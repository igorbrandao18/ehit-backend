# ehit_backend/security_middleware.py

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
import time
import hashlib

class SecurityHeadersMiddleware(MiddlewareMixin):
    """Middleware para adicionar headers de segurança"""
    
    def process_response(self, request, response):
        # Headers de segurança
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'"
        )
        response['Content-Security-Policy'] = csp
        
        return response

class RateLimitMiddleware(MiddlewareMixin):
    """Middleware para rate limiting personalizado"""
    
    def process_request(self, request):
        # Rate limiting para API
        if request.path.startswith('/api/'):
            client_ip = self.get_client_ip(request)
            cache_key = f"rate_limit_{client_ip}"
            
            # Verificar limite (100 requests por hora)
            current_count = cache.get(cache_key, 0)
            if current_count >= 100:
                return HttpResponse("Rate limit exceeded", status=429)
            
            # Incrementar contador
            cache.set(cache_key, current_count + 1, 3600)  # 1 hora
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class SecurityAuditMiddleware(MiddlewareMixin):
    """Middleware para auditoria de segurança"""
    
    def process_request(self, request):
        # Log tentativas de acesso suspeitas
        if self.is_suspicious_request(request):
            self.log_suspicious_activity(request)
        
        return None
    
    def is_suspicious_request(self, request):
        suspicious_patterns = [
            '..',  # Path traversal
            '<script',  # XSS
            'union select',  # SQL injection
            'eval(',  # Code injection
            'base64',  # Encoding attempts
        ]
        
        query_string = str(request.GET) + str(request.POST)
        return any(pattern in query_string.lower() for pattern in suspicious_patterns)
    
    def log_suspicious_activity(self, request):
        import logging
        logger = logging.getLogger('security')
        
        log_data = {
            'ip': self.get_client_ip(request),
            'path': request.path,
            'method': request.method,
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'timestamp': time.time(),
        }
        
        logger.warning(f"Suspicious activity detected: {log_data}")
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
