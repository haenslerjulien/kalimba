from django.urls import path
from .views import LeaderboardAPIView

urlpatterns = [
    path('leaderboard/', LeaderboardAPIView.get_leaderboard),
    path('leaderboard/<int:id>', LeaderboardAPIView.get_user_rank),
]