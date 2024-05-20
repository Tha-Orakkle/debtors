from datetime import timedelta
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from base.models import User
from .error_views import CustomAPIException
from .serializers import UserSerializer


class UserCreateView(APIView):
    """handles the creation of new user"""

    def post(self, request):
        """creates a new user. Returns the user and authentication token"""
        if 'email' not in request.data:
            raise CustomAPIException("Email Missing", status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(email=email)
                user.set_password(request.data.get('password'))
                user.save()
                token = Token.objects.create(user=user)
                return Response({"token": token.key, 'user': serializer.data}, 
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise CustomAPIException("User With Email Already Exists", status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """"Handles the Login"""

    def post(self, request):
        """logs a user in. Return user with authentication 
        token (pulled from db or freshly created)"""
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            current_time = timezone.now()
            if not created and token.created < current_time - timedelta(days=1):
                token.delete()
                token = Token.objects.create(user=user)
            serializer = UserSerializer(instance=user)
            return Response({"token": token.key, "user": serializer.data},
                            status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED) 
