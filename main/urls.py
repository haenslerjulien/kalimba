from django.urls import path
from . import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('samples/', views.SampleAPIView.samples_list),
    path('samples/<int:id>', views.SampleAPIView.sample_handler),
    path('guesses/', views.GuessAPIView.create_guess),
    path('guesses/<int:id>', views.GuessAPIView.guess_handler),
]

urlpatterns = format_suffix_patterns(urlpatterns)