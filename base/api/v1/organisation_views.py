from base.models import Organisation
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from .serializers import OrganisationSerializer
from .helper import get_object
from .error_views import CustomAPIException


class OrganisationView(APIView):
    """API endpoint for requests relating to the Organisation Model """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """gets list of all Organisation objects or 
        specific Organisation object owned by the authenticated user"""
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
        """creates a new organisation"""
        try:
            name = request.data.get('name')
            if not name:
                raise CustomAPIException("Name not valid", status.HTTP_400_BAD_REQUEST)
            if Organisation.objects.get(name=name):
                raise CustomAPIException("Organisation already exists", status.HTTP_400_BAD_REQUEST)
        except Organisation.DoesNotExist:
            serializer = OrganisationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        
    def put(self, request, pk=None):
        if pk is not None:
            organisation = get_object(Organisation, pk)
            serializer = OrganisationSerializer(organisation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None):
        if pk is not None:
            organisation = get_object(Organisation, pk)
            organisation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)