from django.urls import path
from . import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('register/', views.user_register_view),
    path('logout/', views.logout_user)
]

urlpatterns = format_suffix_patterns(urlpatterns)