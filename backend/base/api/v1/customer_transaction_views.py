from decimal import Decimal
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView, Response

from base.models import Customer, Transaction
from .error_views import CustomAPIException
from .helper import strConvertDecimal, updateLaterTransactions
from .serializers import TransactionSerializer


class CustomerTransactionView(APIView):
    """Class Based View for customer-specific transactions"""

    def get(self, request, **kwargs):
        customer = Customer.objects.filter(
            Q(organisation__owner=request.user) & 
            Q(organisation__id=kwargs.get('org_id')) &
            Q(id=kwargs.get('cus_id'))
        ).first()

        if not customer:
            raise CustomAPIException("Invalid Organisation/Customer Id", status.HTTP_400_BAD_REQUEST)
        
        transactions = customer.transaction_set.all()
        
        if transactions and kwargs.get('tran_id'):
            transaction = transactions.filter(id=kwargs['tran_id']).first()
            if not transaction:
                raise CustomAPIException("Transaction Does Not Exist")
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
        

    def post(self, request, **kwargs):
        customer = Customer.objects.filter(
            Q(organisation__owner=request.user) & 
            Q(organisation__id=kwargs.get('org_id')) &
            Q(id=kwargs.get('cus_id'))
        ).first()

        if not customer:
            raise CustomAPIException("Invalid Organisation/Customer Id", status.HTTP_400_BAD_REQUEST)

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
        
        if balance < 0:
            raise CustomAPIException(
                "Amount Paid is higher than prev_mount plus new_amount",
                status.HTTP_400_BAD_REQUEST
            )
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
        customer = Customer.objects.filter(
            Q(organisation__owner=request.user) & 
            Q(organisation__id=kwargs.get('org_id')) &
            Q(id=kwargs.get('cus_id'))
        ).first()

        if not customer:
            raise CustomAPIException("Invalid Organisation/Customer Id", status.HTTP_400_BAD_REQUEST)

        transaction = customer.transaction_set.filter(id=kwargs.get('tran_id')).first()
        if not transaction:
            raise CustomAPIException('Customer Transaction Does Not Exist', status.HTTP_400_BAD_REQUEST)
        
        later_transactions = customer.transaction_set.filter(
            Q(created_at__gt=transaction.created_at)
        )
        transaction_type = request.data.get('transaction_type')
        prev_debt = transaction.prev_amount
        ap = request.data.get('amount_paid')
        amount_paid = strConvertDecimal(ap) if ap else Decimal(0)

        if transaction_type == 'payment':
            if amount_paid == 0:
                raise CustomAPIException("Missing Value", status.HTTP_400_BAD_REQUEST)
            if transaction.prev_amount == 0:
                raise CustomAPIException(
                    "You Cannot Make Payment Where No Transaction Exists",
                    status.HTTP_400_BAD_REQUEST
                )
            transaction.new_amount = Decimal(0)
            transaction.balance = prev_debt - amount_paid
        elif transaction_type == 'new_transaction':
            na = request.data.get('new_amount')
            transaction.new_amount = strConvertDecimal(na)
            transaction.balance = (prev_debt + transaction.new_amount) - amount_paid

        else:
            raise CustomAPIException("Invalid transaction_type", status.HTTP_400_BAD_REQUEST)

        if transaction.balance < 0:
            raise CustomAPIException(
                "Amount Paid is higher than prev_mount plus new_amount",
                status.HTTP_400_BAD_REQUEST
            )
        
        transaction.amount_paid = amount_paid
        transaction.transaction_type = transaction_type
        balance = transaction.balance
        transaction.save()
        updateLaterTransactions(list(later_transactions), balance)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data) 
                
    def delete(self, request, **kwargs):
        customer = Customer.objects.filter(
            Q(organisation__owner=request.user) & 
            Q(organisation__id=kwargs.get('org_id')) &
            Q(id=kwargs.get('cus_id'))
        ).first()

        if not customer:
            raise CustomAPIException("Invalid Organisation/Customer Id", status.HTTP_400_BAD_REQUEST)

        transaction = customer.transaction_set.filter(id=kwargs.get('tran_id')).first()
        if not transaction:
            raise CustomAPIException('Customer Transaction Does Not Exist', status.HTTP_400_BAD_REQUEST)
        
        later_transactions = customer.transaction_set.filter(
            Q(created_at__gt=transaction.created_at)
        )
        balance = transaction.prev_amount
        transaction.delete()
        updateLaterTransactions(list(later_transactions), balance)
        return Response(status=status.HTTP_204_NO_CONTENT)
