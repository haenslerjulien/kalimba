from django.urls import path
from . import views

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', views.user_register_view),
    path('logout/', views.logout_user),
    path('auth/', obtain_auth_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)