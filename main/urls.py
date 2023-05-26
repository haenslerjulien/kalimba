from django.urls import path
from . import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('samples/', views.samples_list),
    path('samples/<int:id>', views.sample_details),
]

urlpatterns = format_suffix_patterns(urlpatterns)