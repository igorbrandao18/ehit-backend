from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.core.cache import cache
import redis
import os

@require_http_methods(["GET"])
@csrf_exempt
def health_check(request):
    """
    Endpoint de health check para monitoramento da aplicação
    """
    health_status = {
        "status": "healthy",
        "timestamp": None,
        "services": {}
    }
    
    try:
        from django.utils import timezone
        health_status["timestamp"] = timezone.now().isoformat()
    except Exception as e:
        health_status["timestamp"] = "unknown"
    
    # Verificar banco de dados
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status["services"]["database"] = {
                "status": "healthy",
                "type": "postgresql"
            }
    except Exception as e:
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "unhealthy"
    
    # Verificar Redis
    try:
        cache.set('health_check', 'ok', 10)
        cache_result = cache.get('health_check')
        if cache_result == 'ok':
            health_status["services"]["redis"] = {
                "status": "healthy",
                "type": "redis"
            }
        else:
            raise Exception("Cache test failed")
    except Exception as e:
        health_status["services"]["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "unhealthy"
    
    # Verificar arquivos estáticos
    try:
        static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')
        if os.path.exists(static_root):
            health_status["services"]["static_files"] = {
                "status": "healthy",
                "path": static_root
            }
        else:
            health_status["services"]["static_files"] = {
                "status": "warning",
                "message": "Static files directory not found"
            }
    except Exception as e:
        health_status["services"]["static_files"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Verificar variáveis de ambiente críticas
    critical_env_vars = ['SECRET_KEY', 'DATABASE_URL']
    missing_vars = []
    for var in critical_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        health_status["services"]["environment"] = {
            "status": "unhealthy",
            "missing_variables": missing_vars
        }
        health_status["status"] = "unhealthy"
    else:
        health_status["services"]["environment"] = {
            "status": "healthy"
        }
    
    # Determinar status HTTP
    if health_status["status"] == "healthy":
        return JsonResponse(health_status, status=200)
    else:
        return JsonResponse(health_status, status=503)
