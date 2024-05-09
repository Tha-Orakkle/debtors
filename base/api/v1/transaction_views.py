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
    


# A Debtors view that returns a list of all debtors with their last transaction

class DebtorsView(APIView):
    def get(self, request):
        sum = Decimal(0)
        debtors = []
        customers = Customer.objects.all()
        for customer in customers:
            customer_tran = customer.transaction_set.first()
            if customer_tran:
                if customer_tran.balance > 0:
                    debtors.append({
                        'name': customer.name,
                        'amount_owed': customer_tran.balance,
                    })
                    sum += customer_tran.balance
        debtors.append({
            'total_debt': sum
        })
        return Response(debtors)
    

class CustomerSearchView(APIView):
    def get(self, request):
        pass