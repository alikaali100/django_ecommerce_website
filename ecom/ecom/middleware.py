from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get("access_token")
        if access_token:
            try:
                token = AccessToken(access_token)  # Validate the token
                request.user = token["user_id"]  # Assuming "user_id" is encoded in the token
            except Exception:
                raise AuthenticationFailed("Invalid or expired access token.")
        else:
            request.user = None
