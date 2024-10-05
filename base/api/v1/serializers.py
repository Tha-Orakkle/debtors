from base.models import Customer, Organisation, Transaction, User
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers


# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class OrganisationSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Organisation
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    organisation = OrganisationSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Transaction
        fields = '__all__'