# cookie_utils.py
from django.http import HttpResponse
# from django.utils.http import urlquote
import datetime

def set_token_cookie(response, token, max_age=3600):
    """
    Set a token in a cookie.
    
    Args:
        response: The HTTP response object.
        token: The token to store in the cookie.
        max_age: The maximum age of the cookie in seconds (default is 1 hour).
    """
    response.set_cookie(
        key='access_token',
        value=token,
        max_age=max_age,
        httponly=True,  # Prevents JavaScript access
        secure=True,    # Use HTTPS
        samesite='Lax'  # CSRF protection
    )
    return response

def get_token_from_cookie(request):
    """
    Get the token from the cookie.
    
    Args:
        request: The HTTP request object.
    
    Returns:
        The token from the cookie, or None if not present.
    """
    return request.COOKIES.get('access_token')
