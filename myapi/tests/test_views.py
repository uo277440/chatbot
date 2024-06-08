import pytest
import os
from rest_framework.test import APIClient,force_authenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from myapi.models import AppUser
import json

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

@pytest.mark.django_db
def test_upload_combined_success(api_client):
    user = AppUser.objects.create_superuser(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)
    
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'test_good_json.json')
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'test_good_csv.csv')
    
    with open(json_path, 'rb') as json_file, open(csv_path, 'rb') as csv_file:
        response = api_client.post(
            reverse('upload_combined'),
            {
                'json_file': json_file,
                'csv_file': csv_file,
                'scenario': 'test_scenario'
            },
            format='multipart'
        )
    response_data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert 'message' in response_data
    assert response_data['message'] == 'Files uploaded and verified successfully'
    assert 'flow' in response_data
    
    
@pytest.mark.django_db
def test_upload_combined_missing_files(api_client):
    user = AppUser.objects.create_superuser(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)
    
    response = api_client.post(
        reverse('upload_combined'),
        {
            'scenario': 'test_scenario'
        },
        format='multipart'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_upload_combined_invalid_json(api_client):
    user = AppUser.objects.create_superuser(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)
    
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'test_good_csv.csv')
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'test_bad_json.json')
    
    
    with open(csv_path, 'rb') as csv_file,open(json_path, 'rb') as json_file :
        response = api_client.post(
            reverse('upload_combined'),
            {
                'json_file': json_file,  
                'csv_file': csv_file,
                'scenario': 'test_scenario'
            },
            format='multipart'
        )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    

@pytest.mark.django_db
def test_upload_combined_invalid_csv(api_client):
    user = AppUser.objects.create_superuser(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)
    
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'test_good_json.json')
    
    with open(json_path, 'rb') as json_file:
        response = api_client.post(
            reverse('upload_combined'),
            {
                'json_file': json_file,
                'csv_file': json_file,  
                'scenario': 'test_scenario'
            },
            format='multipart'
        )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_upload_combined_bad_csv(api_client):
    user = AppUser.objects.create_superuser(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)
    
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'test_good_json.json')
    bad_csv_path = os.path.join(os.path.dirname(__file__), 'data', 'test_bad_csv.csv')
    
    with open(json_path, 'rb') as json_file, open(bad_csv_path, 'rb') as csv_file:
        response = api_client.post(
            reverse('upload_combined'),
            {
                'json_file': json_file,
                'csv_file': csv_file,
                'scenario': 'test_scenario'
            },
            format='multipart'
        )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_upload_combined_bad_json(api_client):
    user = AppUser.objects.create_superuser(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)
    
    bad_json_path = os.path.join(os.path.dirname(__file__), 'data', 'test_bad_json.json')
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'test_good_csv.csv')
    
    with open(bad_json_path, 'rb') as json_file, open(csv_path, 'rb') as csv_file:
        response = api_client.post(
            reverse('upload_combined'),
            {
                'json_file': json_file,
                'csv_file': csv_file,
                'scenario': 'test_scenario'
            },
            format='multipart'
        )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST




    

