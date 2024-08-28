from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

class JWTCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Avoid infinite redirect loop by not applying middleware on login or register pages
        if request.path in ['/login/', '/register/']:
            return None

        access_token = request.COOKIES.get('access_token')
    
        if access_token:
            try:
                # Decode the token to extract user ID
                token = AccessToken(access_token)
                user_id = token['user_id']
                
                # Set the user in the request object
                user = User.objects.get(id=user_id)
                request.user = user

                # Set the authorization header
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

            except User.DoesNotExist:
                # Redirect to registration if the user does not exist
                return redirect('register')
            except Exception as e:
                # Redirect to login if there's any other issue
                return redirect('login')
        else:
            # If no access token is found, redirect to login
            return redirect('login')

        return None  # Allow the request to proceed
