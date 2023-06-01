from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .models import Vote
from main.models import Guess
from .models import VoteType
from .serializers import VoteSerializer
from core.authentication import TokenAuthentication

# # # # # # # # # # # # # # # # #
#          V O T E S            #
# # # # # # # # # # # # # # # # #

class VoteAPIView(APIView):
    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def upvote(request, id, format=None):
        if request.method == 'POST':
            try:
                guess = Guess.objects.get(pk=id)
            except Guess.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if guess.user.id == request.user.id and not request.user.is_superuser:
                raise PermissionDenied('You can\'t vote on your own guess.')
            
            #Has the user already voted ? 
            if Vote.objects.filter(user=request.user.id, guess=guess.id).exists():
                vote = Vote.objects.get(user=request.user.id, guess=guess.id)
                
                #Already upvoted --> delete vote
                if vote.type == VoteType.UP:
                    vote.delete()
                    guess.votecount -= 1
                    guess.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                elif vote.type == VoteType.DOWN:
                    #Upvote the guess
                    vote.type = VoteType.UP
                    vote.save()

                    #Increase guess count
                    # We go from downvote to up, so +2 
                    guess.votecount += 2
                    guess.save()
                    return Response(status=status.HTTP_202_ACCEPTED)
                
            #If the user hasn't voted yet, just create the vote and increase count
            serializer = VoteSerializer(data={'user' : request.user.id, 'guess' : guess.id, 'type' : VoteType.UP})
            if serializer.is_valid():
                serializer.save()
                guess.votecount += 1
                guess.save()
                return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors)
    
    @api_view(['POST'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def downvote(request, id, format=None):
        if request.method == 'POST':
            try:
                guess = Guess.objects.get(pk=id)
            except Guess.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if guess.user.id == request.user.id and not request.user.is_superuser:
                raise PermissionDenied('You can\'t vote on your own guess.')
            
            #Has the user already voted ? 
            if Vote.objects.filter(user=request.user.id, guess=guess.id).exists():
                vote = Vote.objects.get(user=request.user.id, guess=guess.id)

                #Already downvoted --> delete vote
                if vote.type == VoteType.DOWN:
                    vote.delete()
                    guess.votecount += 1
                    guess.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                elif vote.type == VoteType.UP:
                    #Downvote the guess
                    vote.type = VoteType.DOWN
                    vote.save()

                    #Increase guess count
                    # We go from upvote to down, so -2 
                    guess.votecount -= 2
                    guess.save()
                    return Response(status=status.HTTP_202_ACCEPTED)
                
            #If the user hasn't voted yet, just create the vote and decrease count
            serializer = VoteSerializer(data={'user' : request.user.id, 'guess' : guess.id, 'type' : VoteType.DOWN})
            if serializer.is_valid():
                serializer.save()
                guess.votecount -= 1
                guess.save()
                return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors)
        