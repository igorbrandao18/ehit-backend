from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler to return 401 instead of 403 for unauthenticated users
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        # If the response is 403 Forbidden and it's due to authentication
        if response.status_code == status.HTTP_403_FORBIDDEN:
            # Check if it's an authentication issue
            if hasattr(exc, 'detail') and 'Authentication credentials were not provided' in str(exc.detail):
                response.status_code = status.HTTP_401_UNAUTHORIZED
            elif hasattr(exc, 'detail') and 'Invalid token' in str(exc.detail):
                response.status_code = status.HTTP_401_UNAUTHORIZED
    
    return response
