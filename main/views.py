from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, authentication, generics, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .models import Sample
from .serializers import SampleSerializer
from core.authentication import TokenAuthentication

class SampleAPIView(APIView):
    @api_view(['GET', 'POST'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def samples_list(request, format=None):
        if request.method == 'GET':
            samples = Sample.objects.all()
            serializer = SampleSerializer(samples, many=True)
            return Response(serializer.data)
        
        if request.method == 'POST':
            sample = SampleSerializer(data=request.data, context={"request":request})
            if sample.is_valid():
                sample.save()
                return Response(sample.data, status=status.HTTP_201_CREATED)
            
    @api_view(['GET', 'DELETE'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def sample_details(request, id, format=None):
        if request.method == 'GET':
            try:
                sample = Sample.objects.get(pk=id)
            except Sample.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if request.method == 'GET':
                serializer = SampleSerializer(sample)
                return Response(serializer.data)
            
        elif request.method == 'DELETE':
            try:
                sample = Sample.objects.get(pk=id)
            except Sample.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if request.user.id != sample.user.id and not request.user.is_superuser:
                raise PermissionDenied('Trying to delete other people\'s samples ? Not cool')
                
            sample.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        