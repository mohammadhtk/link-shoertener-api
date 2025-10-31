import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthenticationAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        assert response.status_code == 201
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=User.USER
        )
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', data)
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_get_current_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=User.USER
        )
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/auth/me/')
        assert response.status_code == 200
        assert response.data['username'] == 'testuser'


@pytest.mark.django_db
class TestUserManagementAPI:
    def setup_method(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role=User.ADMIN
        )
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123',
            role=User.USER
        )

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/auth/users/')
        assert response.status_code == 200
        assert len(response.data['results']) >= 2

    def test_regular_user_cannot_list_users(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/auth/users/')
        assert response.status_code == 403

    def test_admin_can_delete_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/auth/users/{self.regular_user.id}/')
        assert response.status_code == 204
