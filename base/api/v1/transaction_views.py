from base.models import Customer, Transaction
from decimal import Decimal, InvalidOperation
from rest_framework import status
from rest_framework.views import APIView, Response
from .error_views import CustomAPIException
from .helper import decimalConvertStr
from .serializers import TransactionSerializer


class TransactionView(APIView):

    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise CustomAPIException("Transaction Does Not Exist", status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk=None):
        if pk is not None:
            transaction = self.get_object(pk)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if 'customer' not in request.data:
            raise CustomAPIException("Customer ID Missing", status.HTTP_400_BAD_REQUEST)
        customer_id = request.data.get('customer')
        try:
            customer =  Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise CustomAPIException("Customer Does Not Exist", status.HTTP_400_BAD_REQUEST)
            
        last_transaction = Transaction.objects.filter(customer__id=customer.id).first()
        prev_debt = last_transaction.balance if last_transaction else Decimal(0.0)
        transaction_type = request.data.get('transaction_type')
        ap = request.data.get('amount_paid')
        amount_paid = decimalConvertStr(ap) if ap else Decimal(0)

        if transaction_type == 'payment':
            if amount_paid == 0:
                raise CustomAPIException("Missing Value", status.HTTP_400_BAD_REQUEST)
            new_amount = Decimal(0)
            balance = prev_debt - amount_paid
        elif transaction_type == 'new_transaction':
            na = request.data.get('new_amount')
            new_amount = decimalConvertStr(na)
            balance = (prev_debt + new_amount) - amount_paid
        else:
            raise CustomAPIException("Invalid transaction_type", status.HTTP_400_BAD_REQUEST)
        
        new_transaction = Transaction.objects.create(
                customer=customer,
                transaction_type=transaction_type,
                prev_amount=prev_debt,
                new_amount=new_amount,
                amount_paid=amount_paid,
                balance=balance
            )
        serializer = TransactionSerializer(new_transaction)
        return Response(serializer.data)
    
    def put(self, request, pk=None):
        if pk is None:
            raise CustomAPIException("Invalid Transaction Id", status.HTTP_400_BAD_REQUEST)
        
        

    def delete(self, request, pk=None):
        if pk is not None:
            transaction = self.get_object(pk)
            transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)