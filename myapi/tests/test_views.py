import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return get_user_model().objects.create_user(**kwargs)
    return make_user

@pytest.mark.django_db
def test_user_registration(api_client):
    response = api_client.post(reverse('register'), {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testuser@example.com'
    })
    bad_response = api_client.post(reverse('register'), {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testuser@example.com'
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert bad_response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_user_login(api_client, create_user):
    user = create_user(username='testuser', password='testpassword', email='testuser@example.com')
    response = api_client.post(reverse('login'), {
        'password': 'testpassword',
        'email': 'testuser@example.com'
    })
    empty_response = api_client.post(reverse('login'), {
        'password': '',
        'email': 'testuser@example.com'
    })
    bad_response = api_client.post(reverse('login'), {
        'password': 'incorrect',
        'email': 'testuser@example.com'
    })
    assert response.status_code == status.HTTP_200_OK
    assert empty_response.status_code == status.HTTP_400_BAD_REQUEST
    assert bad_response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_user_logout(api_client, create_user):
    user = create_user(username='testuser', password='testpassword', email='testuser@example.com')
    api_client.force_authenticate(user=user)
    response = api_client.post(reverse('logout'))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_check_chatbot(api_client, create_user):
    user = create_user(username='testuser', password='testpassword', email='testuser@example.com')
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse('check_chatbot'))
    assert response.status_code == status.HTTP_200_OK



