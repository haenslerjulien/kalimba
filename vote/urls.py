from django.urls import path
from .views import VoteAPIView

urlpatterns = [
    path('guesses/<int:id>/upvote', VoteAPIView.upvote),
    path('guesses/<int:id>/downvote', VoteAPIView.downvote),
    path('guesses/<int:id>/approve', VoteAPIView.approve),
]