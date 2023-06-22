import pytest 
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def user():
    user = User(email='verycooluser@mail.com', username='coolUser')
    user.set_password('strongPassword123')
    user.save()

    return user

@pytest.fixture
def client():
    return APIClient()