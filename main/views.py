from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, authentication, generics, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FileUploadParser
from .models import Sample, Guess, Comment
from .serializers import SampleSerializer, GuessSerializer, UpdateGuessSerializer, CommentSerializer, UpdateCommentSerializer
from core.authentication import TokenAuthentication

# # # # # # # # # # # # # # # # #
#       S A M P L E S           #
# # # # # # # # # # # # # # # # #

class SampleAPIView(APIView):

    parser_classes = (FileUploadParser,)

    @api_view(['GET', 'POST'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def samples_list(request, format=None):
        if request.method == 'GET':
            samples = Sample.objects.all()
            serializer = SampleSerializer(samples, many=True)
            return Response(serializer.data)
        
        if request.method == 'POST':
            serializer = SampleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors)
    
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
        

# # # # # # # # # # # # # # # # #
#       G U E S S E S           #
# # # # # # # # # # # # # # # # #
        
class GuessAPIView(APIView):

    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def create_guess(request, format=None):
        if request.method == 'POST':
            try:
                sample = Sample.objects.get(pk=request.data.get('sample'))
            except Sample.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if sample.user.id == request.user.id and not request.user.is_superuser:
                raise PermissionDenied('You can\'t guess on your own sample.')
            
            serializer = GuessSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors)


    @api_view(['DELETE', 'PUT'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def guess_handler(request, id, format=None):
        try:
            guess = Guess.objects.get(pk=id)
        except Guess.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.id != guess.user.id and not request.user.is_superuser:
            raise PermissionDenied('You haven\'t made this guess, so you can\'t modify it.')
        
        if request.method == 'PUT':
            serializer = UpdateGuessSerializer(guess, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors)
        elif request.method == 'DELETE':
            guess.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            

# # # # # # # # # # # # # # # # #
#       C O M M E N T S         #
# # # # # # # # # # # # # # # # #


class CommentApiView(APIView):
    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def create_comment(request, format=None):
        if request.method == 'POST':
            try:
                Guess.objects.get(pk=request.data.get('guess'))
            except Guess.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors)


    @api_view(['DELETE', 'PUT'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def comment_handler(request, id, format=None):
        try:
            comment = Comment.objects.get(pk=id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.id != comment.user.id and not request.user.is_superuser:
            raise PermissionDenied('You haven\'t made this comment, so you can\'t modify it.')
        
        if request.method == 'PUT':
            serializer = UpdateCommentSerializer(comment, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors)
        elif request.method == 'DELETE':
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)