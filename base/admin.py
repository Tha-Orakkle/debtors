from django.contrib import admin
from .models import Customer, Organisation, Transaction
# Register your models here.

admin.site.register(Organisation)
admin.site.register(Customer)
admin.site.register(Transaction)