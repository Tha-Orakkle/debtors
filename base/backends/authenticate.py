from datetime import timedelta
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from base.models import User, CustomToken
from django.contrib.auth.backends import ModelBackend
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import Response 


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class CustomAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = CustomToken.objects.get_or_create(user=user)
        if not created and token.is_expired():
            token.delete()
            CustomToken.objects.create(user=user, expires_at=timedelta(min=5))
        elif created:
            token.expires_at = timezone.now() + timedelta(min=5)
            token.save()
        return Response({"token": token.key})