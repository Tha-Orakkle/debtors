from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    other_name = models.CharField(max_length=32, null=True, blank=True)
    telephone = PhoneNumberField(null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=128, null=True)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return f"<{self.id} : User> {self.email}"
    

class Organisation(models.Model):
    """Represents the Organisation Object"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    address = models.TextField()
    telephone = PhoneNumberField(null=True)
    email = models.EmailField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<{self.id} : Organisation> {self.name}"

class Customer(models.Model):
    """Represents the Customer Object"""
    name = models.CharField(max_length=128)
    telephone = PhoneNumberField(null=True, blank=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return f"<{self.id} : Customer> {self.name}"


# implement mode of payment: cash or bank transaction
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('payment', 'payment'),
        ('new_transaction', 'new_transaction'),
    ]
    MODE_OF_PAYMENT = [
        ('cash', 'cash'),
        ('bank_transaction', 'bank_transaction'),
    ]
    """Represents the Transaction Object"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=16, choices=TRANSACTION_TYPES)
    prev_amount = models.DecimalField(max_digits=11, decimal_places=2, default=Decimal(0))
    new_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True) 
    amount_paid = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    mode_of_payment = models.CharField(max_length=20, choices=MODE_OF_PAYMENT, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    date_of_payment = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"<{self.id} : Transaction>\n{self.customer.name}\
        - Total Amount : {self.new_amount}\
        - Prev Amount  : {self.prev_amount}\
        - Amount Paid  : {self.amount_paid}\
        - Balance      : {self.balance}"
