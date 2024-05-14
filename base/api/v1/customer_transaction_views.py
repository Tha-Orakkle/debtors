from decimal import Decimal
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView, Response
from base.models import Customer, Transaction
from .error_views import CustomAPIException
from .helper import get_object, strConvertDecimal, updateLaterTransactions
from .serializers import TransactionSerializer



class CustomerTransactionView(APIView):
    """Class Based View for customer-specific transactions"""

    def get(self, request, pk=None):
        customer = get_object(Customer, pk)
        customer_transactions = customer.transaction_set.all()
        serializer = TransactionSerializer(customer_transactions, many=True)
        return Response(serializer.data)
        

    def post(self, request, pk=None):
        customer = get_object(Customer, pk=pk)

        last_transaction = customer.transaction_set.first()

        prev_debt = last_transaction.balance if last_transaction else Decimal(0.0)
        transaction_type = request.data.get('transaction_type')
        ap = request.data.get('amount_paid')
        amount_paid = strConvertDecimal(ap) if ap else Decimal(0)
        mode = request.data.get("mode_of_payment") if amount_paid > 0 else None
        if amount_paid > 0:
            if mode != "cash" and mode != "bank_transaction":
                raise CustomAPIException("Invalid Mode Of Payment", status.HTTP_400_BAD_REQUEST)

        if transaction_type == 'payment':
            if not last_transaction:
                raise CustomAPIException(
                    'You Cannot Make Payment Where No Transactions Exist',
                    status.HTTP_400_BAD_REQUEST
                    )
            if amount_paid == 0:
                raise CustomAPIException("Missing Value", status.HTTP_400_BAD_REQUEST)
            new_amount = Decimal(0)
            balance = prev_debt - amount_paid
        elif transaction_type == 'new_transaction':
            na = request.data.get('new_amount')
            new_amount = strConvertDecimal(na)
            balance = (prev_debt + new_amount) - amount_paid
        else:
            raise CustomAPIException("Invalid transaction_type", status.HTTP_400_BAD_REQUEST)
        
        new_transaction = Transaction.objects.create(
                customer=customer,
                transaction_type=transaction_type,
                prev_amount=prev_debt,
                new_amount=new_amount,
                amount_paid=amount_paid,
                mode_of_payment=mode,
                balance=balance

            )
        serializer = TransactionSerializer(new_transaction)
        return Response(serializer.data)
    

    def put(self, request, **kwargs):
        if 'pk' not in kwargs or 'tran_id' not in kwargs:
            raise CustomAPIException('Missing pk/tran_id', status.HTTP_400_BAD_REQUEST)
        customer = get_object(Customer, kwargs['pk'])
        try:
            transaction = customer.transaction_set.get(id=kwargs['tran_id'])
        except Transaction.DoesNotExist:
            raise CustomAPIException('Customer Transaaction Does Not Exist', status.HTTP_400_BAD_REQUEST)
        later_transactions = Transaction.objects.filter(
            (Q(customer__id=customer.id) & Q(created_at__gt=transaction.created_at))
        )
        transaction_type = request.data.get('transaction_type')
        prev_debt = transaction.prev_amount
        ap = request.data.get('amount_paid')
        amount_paid = strConvertDecimal(ap) if ap else Decimal(0)

        if transaction_type == 'payment':
            if amount_paid == 0:
                raise CustomAPIException("Missing Value", status.HTTP_400_BAD_REQUEST)
            transaction.new_amount = Decimal(0)
            transaction.balance = prev_debt - amount_paid
        elif transaction_type == 'new_transaction':
            na = request.data.get('new_amount')
            transaction.new_amount = strConvertDecimal(na)
            transaction.balance = (prev_debt + transaction.new_amount) - amount_paid
        else:
            raise CustomAPIException("Invalid transaction_type", status.HTTP_400_BAD_REQUEST)
        
        transaction.amount_paid = amount_paid
        transaction.transaction_type = transaction_type
        balance = transaction.balance
        transaction.save()
        updateLaterTransactions(list(later_transactions), balance)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data) 
                
    def delete(self, request, **kwargs):
        if 'pk' not in kwargs or 'tran_id' not in kwargs:
            raise CustomAPIException('Missing pk/tran_id', status.HTTP_400_BAD_REQUEST)
        customer = get_object(Customer, kwargs['pk'])
        try:
            transaction = customer.transaction_set.get(id=kwargs['tran_id'])
        except Transaction.DoesNotExist:
            raise CustomAPIException('Customer Transaaction Does Not Exist', status.HTTP_400_BAD_REQUEST)
        
        later_transactions = Transaction.objects.filter(
            (Q(customer__id=customer.id) & Q(created_at__gt=transaction.created_at))
        )
        balance = transaction.prev_amount
        transaction.delete()
        updateLaterTransactions(list(later_transactions), balance)
        return Response(status=status.HTTP_204_NO_CONTENT)
