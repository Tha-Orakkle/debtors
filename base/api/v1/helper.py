from decimal import Decimal, InvalidOperation
from rest_framework import status
from .error_views import CustomAPIException

def decimalConvertStr(s):
    try:
        return Decimal(s)
    except (TypeError, InvalidOperation) as e:
        raise CustomAPIException("Invalid Value", status.HTTP_400_BAD_REQUEST)
