import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from users.models import Role, Permission

User = get_user_model()


@pytest.mark.django_db
class TestAuthenticationAPI:
    def setup_method(self):
        self.client = APIClient()
        # Setup roles
        self.user_role = Role.objects.create(name=Role.USER)
        self.admin_role = Role.objects.create(name=Role.ADMIN)

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = self.client.post('/api/users/register/', data)
        assert response.status_code == 201
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_user(self):
        # Create user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=self.user_role
        )

        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/users/login/', data)
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_get_current_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=self.user_role
        )
        self.client.force_authenticate(user=user)

        response = self.client.get('/api/users/me/')
        assert response.status_code == 200
        assert response.data['username'] == 'testuser'


@pytest.mark.django_db
class TestUserManagementAPI:
    def setup_method(self):
        self.client = APIClient()
        # Setup roles and permissions
        self.admin_role = Role.objects.create(name=Role.ADMIN)
        self.user_role = Role.objects.create(name=Role.USER)

        manage_users_perm = Permission.objects.create(
            name='Manage Users',
            code='manage_users'
        )
        self.admin_role.permissions.add(manage_users_perm)

        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role=self.admin_role
        )

        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123',
            role=self.user_role
        )

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/users/users/')
        assert response.status_code == 200
        assert len(response.data['results']) >= 2

    def test_regular_user_cannot_list_users(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/users/users/')
        assert response.status_code == 403

    def test_admin_can_delete_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/users/users/{self.regular_user.id}/')
        assert response.status_code == 204
