from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, authentication, generics, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FileUploadParser
from ..models import Sample
from ..serializers.sample_serializers import SampleSerializer, PostSampleSerializer, GetSampleFileSerializer
from core.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema

# # # # # # # # # # # # # # # # #
#       S A M P L E S           #
# # # # # # # # # # # # # # # # #

class SampleAPIView(APIView):

    parser_classes = (FileUploadParser,)

    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    @extend_schema(
        request=PostSampleSerializer,
        responses={201: SampleSerializer, 404: 'Bad Request'},
        description='Post a new sample',
        methods=["POST"]
    )
    @extend_schema(
        responses={200: SampleSerializer(many=True)},
        description='Get all the samples',
        methods=["GET"]
    )
    @api_view(['GET', 'POST'])
    def samples_list(request):
        if request.method == 'GET':
            samples = Sample.objects.all()
            serializer = SampleSerializer(samples, many=True)
            return Response(serializer.data)
        
        if request.method == 'POST':
            serializer = PostSampleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(SampleSerializer(data=serializer.data), status=status.HTTP_201_CREATED)

        return Response(serializer.errors)
    
    @extend_schema(
        responses={200: FileResponse, 404: 'Not Found'},
        description='Get the audio file for a sample',
        methods=["GET"]
    )
    @extend_schema(
        responses={403: 'Trying to delete someone elses sample', 404: 'Not found', 204: 'No content'},
        description='Delete a sample',
        methods=["DELETE"]
    )
    @api_view(['GET', 'DELETE'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def sample_handler(request, id, format=None):
        if request.method == 'GET':
            try:
                sample = Sample.objects.get(pk=id)
            except Sample.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if request.method == 'GET':
                return FileResponse(sample.file.open())
            
        elif request.method == 'DELETE':
            try:
                sample = Sample.objects.get(pk=id)
            except Sample.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if request.user.id != sample.user.id and not request.user.is_superuser:
                raise PermissionDenied('Trying to delete other people\'s samples ? Not cool')
                
            sample.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        