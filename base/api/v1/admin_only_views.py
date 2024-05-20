from base.models import User, Transaction
from rest_framework import status
from rest_framework.views import APIView, Response
from .error_views import CustomAPIException
from .serializers import TransactionSerializer, UserSerializer


class UserView(APIView):
    # THIS SHOULD ONLY BE ACCESSED BY ADMINS
    """Handles requests relating to the User Model"""

    def get(self, request, pk=None):
        """gets a list of all users or a specific user"""
        if pk is not None:
            user = User.objects.get(id=pk)
            if not user:
                raise CustomAPIException(
                    "Invalid User Id",
                    status.HTTP_400_BAD_REQUEST
                )
            serializer = UserSerializer(user)
            return Response(serializer.data)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class TransactionView(APIView):
    # ALL TRANSACTIONS SHOULD BE ACCESIBLE BY ONLY ADMIN
        
    def get(self, request, pk=None):
        if pk is not None:
            transaction = Transaction.objects.get(id=pk)
            if transaction:
                raise CustomAPIException(
                    "Invalid Transaction Id",
                    status.HTTP_400_BAD_REQUEST
                )
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    

class CustomerSearchView(APIView):
    def get(self, request):
        # To be implemented
        pass