from base.models import Customer, Transaction
from decimal import Decimal
from rest_framework import status
from rest_framework.views import APIView, Response
from .error_views import CustomAPIException
from .helper import get_object, strConvertDecimal
from .serializers import TransactionSerializer


class TransactionView(APIView):
        
    def get(self, request, pk=None):
        if pk is not None:
            transaction = get_object(Transaction, pk)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data) 
