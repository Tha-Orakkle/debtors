from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Organisation(models.Model):
    """Represents the Organisation Object"""
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # owner cannot be nullable
    name = models.CharField(max_length=128)
    address = models.TextField()
    telephone = PhoneNumberField(null=True)
    email = models.EmailField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<{self.id} : Organisation> {self.name}"

class Customer(models.Model):
    """Represents the Customer Object"""
    name = models.CharField(max_length=128)
    telephone = PhoneNumberField(null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True) # organisation cannot be nullable

    def __str__(self):
        return f"<{self.id} : Customer> {self.name}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('payment', 'payment'),
        ('new_transaction', 'new_transaction'),
    ]
    """Represents the Transaction Object"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=16, choices=TRANSACTION_TYPES)
    prev_amount = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    new_amount = models.DecimalField(max_digits=11, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    balance = models.DecimalField(max_digits=11, decimal_places=2)
    date_of_payment = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"<{self.id} : Transaction> {self.customer.name}\n \
        - Total Amount : {self.new_amount}\n \
        - Amount Paid  : {self.amount_paid}\n \
        - Balance      : {self.balance}\n "
    
