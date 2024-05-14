from django.contrib import admin
from .models import Customer, Organisation, Transaction, User
# Register your models here.

admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(Customer)
admin.site.register(Transaction)