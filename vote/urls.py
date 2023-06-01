from django.urls import path
from .views import VoteAPIView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('guesses/<int:id>/upvote', VoteAPIView.upvote),
    path('guesses/<int:id>/downvote', VoteAPIView.downvote),
]

urlpatterns = format_suffix_patterns(urlpatterns)