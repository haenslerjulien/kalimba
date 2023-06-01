from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, authentication, generics, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from ..models import Guess, Comment
from ..serializers.comment_serializers import CommentSerializer, UpdateCommentSerializer
from core.authentication import TokenAuthentication

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