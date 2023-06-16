from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from core.authentication import TokenAuthentication
from django.contrib.auth.models import User
from leaderboard.services.leaderboard_caching import get_user_key, get_redis_instance

# # # # # # # # # # # # # # # # #
#    L E A D E R B O A R D      #
# # # # # # # # # # # # # # # # #

class LeaderboardAPIView(APIView):
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def get_leaderboard(request, format=None):
        if request.method == 'GET':
            r = get_redis_instance()
            leaderboard = r.zrevrange("players:score", 0, -1, withscores=True)
            
            formatted_leaderboard = [
                {
                    "username": userkey.decode().split(":")[0],
                    "user_id": userkey.decode().split(":")[1],
                    "score": score,
                    "rank": rank,
                } for rank, (userkey, score) in enumerate(leaderboard, start=1)
            ]

            return Response(formatted_leaderboard)
        
    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    @authentication_classes([authentication.SessionAuthentication, TokenAuthentication])
    def get_user_rank(request, id, format=None):
        if request.method == 'GET':

            try:
                user = User.objects.get(id=id)
            except  User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            user_key = get_user_key(user)

            r = get_redis_instance()
            rank = r.zrevrank("players:score", user_key) + 1 # Because zrevrank on the highest rank player will return 0
            score = r.zscore("players:score", user_key)
            
            formatted_rank = {
                "username": user.username,
                "user_id": user.id,
                "score": score,
                "rank": rank,
            }

            return Response(formatted_rank)
    
    