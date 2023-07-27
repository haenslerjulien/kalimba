from django.urls import path
from .views import sample_views, guess_views, comment_views

urlpatterns = [
    path('samples/', sample_views.SampleAPIView.samples_list),
    path('samples/<int:id>', sample_views.SampleAPIView.sample_handler),
    path('guesses/', guess_views.GuessAPIView.create_guess),
    path('guesses/<int:id>', guess_views.GuessAPIView.guess_handler),
    path('comments/', comment_views.CommentApiView.create_comment),
    path('comments/<int:id>', comment_views.CommentApiView.comment_handler),
]