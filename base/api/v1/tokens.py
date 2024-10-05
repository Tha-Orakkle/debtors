from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.authtoken.models import Token

from base.models import User


class TokenGenerationView(APIView):
    
    def post(self, request):
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        
        token, created = Token.objects.get_or_create(user=user)
        current_time = timezone.now()
        if not created and token.created < current_time - timedelta(seconds=15):
                token.delete()
                token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)