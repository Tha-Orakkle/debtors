from base.models import User
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class ExpiredTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        print("This is being used")
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")
        
        current_time = timezone.now()
        if token.created < current_time - timedelta(days=1):
            raise AuthenticationFailed("Token Has Expired")

        return token.user, token