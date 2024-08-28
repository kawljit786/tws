# utils.py
from rest_framework_simplejwt.tokens import RefreshToken

def generate_jwt_tokens(user):
    """
    Generate JWT tokens for the given user.
    
    Args:
        user: The user for whom to generate the tokens.
    
    Returns:
        A dictionary containing the refresh and access tokens as strings.
    """
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return {
        'access': access_token,
        'refresh': refresh_token
    }
