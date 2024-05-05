from base.models import Customer, Organisation, Transaction
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


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