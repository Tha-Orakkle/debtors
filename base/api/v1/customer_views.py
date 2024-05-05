from base.models import Customer
from rest_framework import status
from rest_framework.views import APIView, Response
from .error_views import CustomAPIException
from .serializers import CustomerSerializer

class CustomerView(APIView):
    """Customer Model API endpoints"""
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise CustomAPIException("Customer Does not Exist", status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk=None):
        if pk is not None:
            customer = self.get_object(pk)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    # some changes to be effected
    # validating the organisation the customer is under before creating the customer object
    def post(self, request): 
        """creates a new customer"""
        try:
            name = request.data.get('name')
            if not name:
                raise CustomAPIException("Name not valid", status.HTTP_400_BAD_REQUEST)
            if Customer.objects.get(name=name):
                raise CustomAPIException("Customer already exists", status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        
    def put(self, request, pk=None):
        if pk is not None:
            customer = self.get_object(pk)
            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk=None):
        if pk is not None:
            customer = self.get_object(pk)
            customer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        