from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from base.backends.authenticate import ExpiredTokenAuthentication    
from base.models import Customer
from .error_views import CustomAPIException
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
            if not customer:
                raise CustomAPIException("Invalid Customer Id", status.HTTP_400_BAD_REQUEST)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        customers = organisation.customer_set.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


    # POST request endppoint implementation completed
    def post(self, request, org_id=None):
        organisation = request.user.organisation_set.filter(id=org_id).first()
        if not organisation:
            raise CustomAPIException("Invalid Organisation Id", status.HTTP_400_BAD_REQUEST)
        if not request.data.get('name'):
            raise CustomAPIException("Name not valid", status.HTTP_400_BAD_REQUEST)
        name = request.data['name'].title().strip()
        try:
            if organisation.customer_set.filter(name=name):
                raise CustomAPIException("Customer already exists", status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            pass
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['name'] = name
            serializer.validated_data['organisation'] = organisation
            serializer.save()
            print("Execution Got to this point")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

        
    def put(self, request, org_id=None, cus_id=None):
        organisation = request.user.organisation_set.filter(id=org_id).first()
        if not organisation:
            raise CustomAPIException("Invalid Organisation Id", status.HTTP_400_BAD_REQUEST)
        customer = organisation.customer_set.filter(id=cus_id).first()
        if not customer:
            raise CustomAPIException("Invalid Customer Id", status.HTTP_400_BAD_REQUEST)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['name'] = serializer.validated_data['name'].lower().strip()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, org_id=None, cus_id=None):
        organisation = request.user.organisation_set.filter(id=org_id).first()
        if not organisation:
            raise CustomAPIException("Invalid Organisation Id", status.HTTP_400_BAD_REQUEST)
        customer = organisation.customer_set.filter(id=cus_id).first()
        if not customer:
            raise CustomAPIException("Invalid Customer Id", status.HTTP_400_BAD_REQUEST)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        