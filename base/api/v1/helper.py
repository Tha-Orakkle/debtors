from decimal import Decimal, InvalidOperation
from rest_framework import status
from base.models import Organisation, Customer, Transaction
from .error_views import CustomAPIException


def strConvertDecimal(s):
    try:
        return Decimal(s)
    except (TypeError, InvalidOperation) as e:
        raise CustomAPIException("Invalid Value", status.HTTP_400_BAD_REQUEST)
    

def get_object(cls, pk):
    classes = [
        Customer,
        Organisation,
        Transaction,
    ]
    if cls in classes:
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            detail = "{} Does Not Exist".format(cls.__name__)
            raise CustomAPIException(detail, status.HTTP_400_BAD_REQUEST)


def updateLaterTransactions(transactions, balance):
    if not transactions:
        return
    next_transaction = transactions.pop()
    next_transaction.prev_amount = balance
    print('---------------')
    print(next_transaction.prev_amount)
    print('---------------')
    if next_transaction.transaction_type == 'payment':
        balance = next_transaction.prev_amount - next_transaction.amount_paid
        print(balance)
    elif next_transaction.transaction_type == 'new_transaction':
        balance = (next_transaction.prev_amount + next_transaction.new_amount) - next_transaction.amount_paid
        print(balance)
    next_transaction.balance =  balance
    next_transaction.save()
    updateLaterTransactions(transactions, balance)
