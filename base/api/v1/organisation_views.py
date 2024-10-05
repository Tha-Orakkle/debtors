from decimal import Decimal
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from .serializers import OrganisationSerializer, TransactionSerializer
from .error_views import CustomAPIException
from base.backends.authenticate import ExpiredTokenAuthentication
from base.models import Organisation

class OrganisationView(APIView):
    """API endpoint for requests for Organisations"""
    authentication_classes = [ExpiredTokenAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """Gets Lists of Organisation Objects owned by authenticated user"""
        user = request.user
        if pk is not None:
            organisation = user.organisation_set.filter(id=pk).first()
            if not organisation:
                raise CustomAPIException("Organisation Does Not Exist", status.HTTP_400_BAD_REQUEST)
            serializer = OrganisationSerializer(organisation)
            return Response(serializer.data)
        organisations = user.organisation_set.all()
        serializer = OrganisationSerializer(organisations, many=True)
        return Response(serializer.data)

    
    # some changes to be effected
    # validating the owner of the organisation before creating the organisation object
    def post(self, request):
        """Creates a New Organisation Object"""
        user = request.user
        try:
            name = request.data.get('name')
            if not name:
                raise CustomAPIException("Name not valid", status.HTTP_400_BAD_REQUEST)
            if Organisation.objects.get(name=name):
                raise CustomAPIException("Organisation already exists", status.HTTP_400_BAD_REQUEST)
        except Organisation.DoesNotExist:
            serializer = OrganisationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['owner'] = user
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        
    def put(self, request, pk=None):
        """Updates an Organisation Object"""
        organisation = request.user.organisation_set.filter(id=pk).first()
        if not organisation:
            raise CustomAPIException("Organisation Does Not Exist", status.HTTP_400_BAD_REQUEST)
        serializer = OrganisationSerializer(organisation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None):
        """Delete an Organisation Object"""
        organisation = request.user.organisation_set.filter(id=pk).first()
        if not organisation:
            raise CustomAPIException("Organisation Does Not Exist", status.HTTP_400_BAD_REQUEST)
        organisation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DebtorsView(APIView):
    def get(self, request, org_id=None):
        """this endpoint will return a list of all still owing debtors
        this will be in form of the last transaction of all the customers"""
        organisation = Organisation.objects.filter(
            Q(owner=request.user) & Q(id=org_id)
        ).first()
        sum = Decimal(0)
        debtors = []
        customers = organisation.customer_set.all()
        for customer in customers:
            customer_tran = customer.transaction_set.first()
            if customer_tran:
                if customer_tran.balance > 0:
                    debtors.append(customer_tran)
                    sum += customer_tran.balance
        serializer = TransactionSerializer(debtors, many=True)
        return Response({
            "total_debt": sum,
            "debtors": serializer.data
        })
    
