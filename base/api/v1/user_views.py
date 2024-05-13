from django.contrib.auth import authenticate
from rest_framework.views import APIView, Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from base.models import User
from .error_views import CustomAPIException
from .helper import get_object
from .serializers import UserSerializer


class UserCreateView(APIView):
    def post(self, request):
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
                token = Token.objects.create(user=user)
                return Response(
                    {
                        "token": token.key,
                        'user': serializer.data
                        },
                    status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise CustomAPIException("User With Email Already Exists", status.HTTP_400_BAD_REQUEST)
    
class UserSignInView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            raise CustomAPIException('User Does Not Exist', status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        print(user)
        if user is None:
            raise CustomAPIException('Invalid Email/Password', status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    
    
    
    

class UserView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            user = get_object(User, pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)