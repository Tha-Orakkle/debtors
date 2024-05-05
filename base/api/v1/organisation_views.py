from base.models import Organisation
from .serializers import OrganisationSerializer
from .error_views import CustomAPIException
from rest_framework import status
from rest_framework.views import APIView, Response

class OrganisationView(APIView):
    """API endpoint for the Organisation"""

    def get_object(self, pk):
        try:
            return Organisation.objects.get(pk=pk)
        except Organisation.DoesNotExist:
            raise CustomAPIException("Organisation Does Not Exist", status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk is not None:
            organisation = self.get_object(pk)
            serializer = OrganisationSerializer(organisation)
            return Response(serializer.data)
        
        organisations = Organisation.objects.all()
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
            organisation = self.get_object(pk)
            serializer = OrganisationSerializer(organisation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None):
        if pk is not None:
            organisation = self.get_object(pk)
            organisation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)