import pytest
from rest_framework.authtoken.models import Token
from rest_framework import status

@pytest.mark.django_db
def test_register_user(client):
    payload = {
        'username' : 'coolUser', 
        'email' : 'verycooluser@mail.com', 
        'password' : 'strongPassword123', 
        'password2' : 'strongPassword123'
    }

    response = client.post('/register/', payload)

    assert response.status_code == status.HTTP_200_OK

    data = response.data

    assert data['username'] == payload['username']
    assert data['email'] == payload['email']
    assert "password" not in data
    assert data['token'] == Token.objects.all().first().key

@pytest.mark.django_db
def test_register_user_password_not_corresponding(client):
    payload = {
        'username' : 'coolUser', 
        'email' : 'verycooluser@mail.com', 
        'password' : 'strongPassword123', 
        'password2' : 'strongPassword124'
    }

    response = client.post('/register/', payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.data['Error'] == 'Password does not match'

@pytest.mark.django_db
def test_register_user_email_already_exists(client, user):
    
    payload = {
        'username' : 'coolUser2', 
        'email' : 'verycooluser@mail.com', 
        'password' : 'strongPassword123', 
        'password2' : 'strongPassword123'
    }

    response = client.post('/register/', payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.data['Error'] == 'Email already exists'

@pytest.mark.django_db
def test_register_user_username_already_exists(client, user):
    
    payload = {
        'username' : 'coolUser', 
        'email' : 'verycooluser2@mail.com', 
        'password' : 'strongPassword123', 
        'password2' : 'strongPassword123'
    }

    response = client.post('/register/', payload)

    assert response.status_code == status.HTTP_200_OK # ?? why 200 drf ?

    assert response.data['username'][0] == 'A user with that username already exists.'


