from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, authentication, generics, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from ..models import Guess, Sample
from ..serializers.guess_serializers import GuessSerializer, UpdateGuessSerializer
from core.authentication import TokenAuthentication

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
            
