from django.urls import path
from .views import LeaderboardAPIView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('leaderboard/', LeaderboardAPIView.get_leaderboard),
    path('leaderboard/<int:id>', LeaderboardAPIView.get_user_rank),
]

urlpatterns = format_suffix_patterns(urlpatterns)