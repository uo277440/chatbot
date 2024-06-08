import pytest
import os
from rest_framework.test import APIClient,force_authenticate
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from myapi.models import AppUser,Flow,Scenery,ForumMessage,Mark
import json

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return get_user_model().objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def authenticated_user(api_client):
    user = AppUser.objects.create_superuser(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)
    return user
@pytest.fixture
def default_user(api_client):
    user = AppUser.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)
    return user

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
    
@pytest.mark.django_db
def test_delete_flow_success(api_client, create_user):
    user = AppUser.objects.create_superuser(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)

    scenario = Scenery.objects.create(name="test_scenario")
    flow = Flow.objects.create(name="test_flow", scenery=scenario)
    
    response = api_client.post(reverse('delete_flow'), {'flow_id': flow.id})

    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Flow deleted successfully'

@pytest.mark.django_db
def test_delete_flow_missing_flow_id(api_client, create_user):
    user = AppUser.objects.create_superuser(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)

    response = api_client.post(reverse('delete_flow'))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'Flow ID is required'

@pytest.mark.django_db
def test_delete_flow_not_found(api_client, create_user):
    user = AppUser.objects.create_superuser(username='testuser', email='testuser@example.com', password='testpassword')
    api_client.force_authenticate(user=user)

    response = api_client.post(reverse('delete_flow'), {'flow_id': 999})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == 'Flow not found'

@pytest.mark.django_db
def test_get_flows_by_scenario_success(api_client, create_user):
    user = create_user(username='testuser', password='testpassword', email='testuser@example.com')
    api_client.force_authenticate(user=user)

    scenario = Scenery.objects.create(name="test_scenario")
    Flow.objects.create(name="test_flow_1", scenery=scenario)
    Flow.objects.create(name="test_flow_2", scenery=scenario)

    response = api_client.get(reverse('get_flows_by_scenario', args=["test_scenario"]))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['flows']) == 2
    assert response.data['flows'][0]['name'] == 'test_flow_1'
    assert response.data['flows'][1]['name'] == 'test_flow_2'

@pytest.mark.django_db
def test_get_flows_by_scenario_not_found(api_client, create_user):
    user = create_user(username='testuser', password='testpassword', email='testuser@example.com')
    api_client.force_authenticate(user=user)

    response = api_client.get(reverse('get_flows_by_scenario', args=["non_existing_scenario"]))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == 'Scenario not found'
@pytest.mark.django_db
def test_delete_message_success(api_client, authenticated_user):
    message = ForumMessage.objects.create(user=authenticated_user, message="Test message")
    
    response = api_client.delete(reverse('delete_message', args=[message.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ForumMessage.objects.filter(id=message.id).count() == 0

@pytest.mark.django_db
def test_delete_message_not_found(api_client, authenticated_user):
    response = api_client.delete(reverse('delete_message', args=[999]))

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_edit_message_success(api_client, authenticated_user):
    message = ForumMessage.objects.create(user=authenticated_user, message="Test message")
    updated_message_data = {'message': 'Updated message'}

    response = api_client.put(reverse('edit_message', args=[message.id]), updated_message_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == updated_message_data['message']
    assert ForumMessage.objects.get(id=message.id).message == updated_message_data['message']

@pytest.mark.django_db
def test_edit_message_not_found(api_client, authenticated_user):
    updated_message_data = {'message': 'Updated message'}

    response = api_client.put(reverse('edit_message', args=[999]), updated_message_data, format='json')

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_forum_messages(api_client, authenticated_user):
    pinned_message = ForumMessage.objects.create(user=authenticated_user, message="Pinned message", pinned=True)
    message1 = ForumMessage.objects.create(user=authenticated_user, message="Test message 1")
    message2 = ForumMessage.objects.create(user=authenticated_user, message="Test message 2")

    response = api_client.get(reverse('forum_messages'))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['messages']) == 3
    assert response.data['pinnedMessage']['message'] == pinned_message.message
@pytest.mark.django_db
def test_user_profile(api_client, authenticated_user):
    scenery = Scenery.objects.create(name='Test Scenery')
    
    flow1 = Flow.objects.create(name='Flow 1', scenery=scenery)
    flow2 = Flow.objects.create(name='Flow 2', scenery=scenery)
    
    Mark.objects.create(user=authenticated_user, flow=flow1, mark=7.5)
    Mark.objects.create(user=authenticated_user, flow=flow1, mark=8.0)
    Mark.objects.create(user=authenticated_user, flow=flow2, mark=6.0)

    response = api_client.get(reverse('user_profile'))

    assert response.status_code == status.HTTP_200_OK
    assert 'user' in response.data
    assert 'average_marks' in response.data
    assert len(response.data['average_marks']) == 2

    average_marks_data = response.data['average_marks']
    flow1_avg_mark = next((mark for mark in average_marks_data if mark['flow']['name'] == 'Flow 1'), None)
    flow2_avg_mark = next((mark for mark in average_marks_data if mark['flow']['name'] == 'Flow 2'), None)

    assert flow1_avg_mark is not None
    assert flow1_avg_mark['average_mark'] == 7.75

    assert flow2_avg_mark is not None
    assert flow2_avg_mark['average_mark'] == 6.0

@pytest.mark.django_db
def test_user_profile_no_marks(api_client, authenticated_user):
    response = api_client.get(reverse('user_profile'))

    assert response.status_code == status.HTTP_200_OK
    assert 'user' in response.data
    assert 'average_marks' in response.data
    assert len(response.data['average_marks']) == 0
@pytest.mark.django_db
def test_search_student_success(api_client, authenticated_user):
    # Crear otro usuario para buscar
    searched_user = AppUser.objects.create_user(username='searcheduser', email='searcheduser@example.com', password='testpassword')
    
    # Crear un escenario y flujos para el usuario buscado
    scenery = Scenery.objects.create(name='Test Scenery')
    flow = Flow.objects.create(name='Test Flow', scenery=scenery)
    
    # Crear marcas para el usuario buscado
    Mark.objects.create(user=searched_user, flow=flow, mark=8.5)
    Mark.objects.create(user=searched_user, flow=flow, mark=9.0)
    
    response = api_client.get(reverse('search_student'), {'search_param': 'searcheduser'})

    assert response.status_code == status.HTTP_200_OK
    assert 'user' in response.data
    assert 'marks' in response.data
    assert response.data['user']['username'] == 'searcheduser'
    assert len(response.data['marks']) == 2

@pytest.mark.django_db
def test_search_student_not_found(api_client, authenticated_user):
    response = api_client.get(reverse('search_student'), {'search_param': 'nonexistentuser'})
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'error' in response.data
    assert response.data['error'] == 'User not found'

@pytest.mark.django_db
def test_search_student_missing_param(api_client, authenticated_user):
    response = api_client.get(reverse('search_student'))
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data
    assert response.data['error'] == 'Username parameter is required'




    

