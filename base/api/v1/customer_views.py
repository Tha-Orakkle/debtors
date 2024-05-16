from base.models import Customer
from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from base.backends.authenticate import ExpiredTokenAuthentication    
from .error_views import CustomAPIException
from .helper import get_object
from .serializers import CustomerSerializer

class CustomerView(APIView):
    """Customer Model API endpoints"""
    authentication_classes = [ExpiredTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, org_id=None, cus_id=None): # test this endpoint
        user = request.user
        if org_id is None:
            raise CustomAPIException("Invalid Organisation Id", status.HTTP_400_BAD_REQUEST)
        organisation = user.organisation_set.filter(id=org_id).first()
        if not organisation:
            raise CustomAPIException("Invalid Organisation Id", status.HTTP_400_BAD_REQUEST)
        if cus_id is not None:
            customer = organisation.customer_set.filter(id=cus_id).first()
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        customers = organisation.customer_set.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)



    # def get(self, request, pk=None):
    #     user = request.user
        
    #     if pk is not None:
    #         customer = get_object(Customer, pk)
    #         serializer = CustomerSerializer(customer)
    #         return Response(serializer.data)
    #     customers = Customer.objects.all()
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)
    
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
            customer = get_object(Customer, pk)
            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk=None):
        if pk is not None:
            customer = get_object(Customer, pk)
            customer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        