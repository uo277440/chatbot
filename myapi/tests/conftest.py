import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user