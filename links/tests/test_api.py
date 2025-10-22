import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from users.models import Role, Permission
from links.models import Link

User = get_user_model()


@pytest.mark.django_db
class TestLinkAPI:
    def setup_method(self):
        self.client = APIClient()

        # Setup roles and permissions
        self.user_role = Role.objects.create(name=Role.USER)
        self.admin_role = Role.objects.create(name=Role.ADMIN)

        # Add permissions
        add_note_perm = Permission.objects.create(name='Add Note', code='add_note')
        edit_link_perm = Permission.objects.create(name='Edit Link', code='edit_link')
        view_stats_perm = Permission.objects.create(name='View Stats', code='view_stats')
        manage_all_perm = Permission.objects.create(name='Manage All Links', code='manage_all_links')

        self.user_role.permissions.add(add_note_perm, edit_link_perm, view_stats_perm)
        self.admin_role.permissions.add(add_note_perm, edit_link_perm, view_stats_perm, manage_all_perm)

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=self.user_role
        )

        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role=self.admin_role
        )

    def test_guest_can_create_link(self):
        # Guest (unauthenticated) can create links
        data = {
            'original_url': 'https://example.com'
        }
        response = self.client.post('/api/links/', data)
        assert response.status_code == 201
        assert 'short_code' in response.data

    def test_guest_can_create_link_with_custom_alias(self):
        data = {
            'original_url': 'https://example.com',
            'custom_alias': 'mylink'
        }
        response = self.client.post('/api/links/', data)
        assert response.status_code == 201
        assert response.data['custom_alias'] == 'mylink'

    def test_guest_cannot_add_note(self):
        data = {
            'original_url': 'https://example.com',
            'note': 'This is a note'
        }
        response = self.client.post('/api/links/', data)
        assert response.status_code == 403

    def test_user_can_add_note(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'original_url': 'https://example.com',
            'note': 'This is a note'
        }
        response = self.client.post('/api/links/', data)
        assert response.status_code == 201
        assert response.data['note'] == 'This is a note'

    def test_user_can_edit_own_link(self):
        self.client.force_authenticate(user=self.user)

        # Create link
        link = Link.objects.create(
            short_code='abc123',
            original_url='https://example.com',
            user=self.user
        )

        # Edit link
        data = {'original_url': 'https://newurl.com'}
        response = self.client.patch(f'/api/links/{link.id}/', data)
        assert response.status_code == 200
        assert response.data['original_url'] == 'https://newurl.com'

    def test_user_cannot_edit_others_link(self):
        other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass123',
            role=self.user_role
        )

        link = Link.objects.create(
            short_code='abc123',
            original_url='https://example.com',
            user=other_user
        )

        self.client.force_authenticate(user=self.user)
        data = {'original_url': 'https://newurl.com'}
        response = self.client.patch(f'/api/links/{link.id}/', data)
        assert response.status_code == 403

    def test_admin_can_edit_any_link(self):
        link = Link.objects.create(
            short_code='abc123',
            original_url='https://example.com',
            user=self.user
        )

        self.client.force_authenticate(user=self.admin)
        data = {'original_url': 'https://newurl.com'}
        response = self.client.patch(f'/api/links/{link.id}/', data)
        assert response.status_code == 200

    def test_admin_can_deactivate_link(self):
        link = Link.objects.create(
            short_code='abc123',
            original_url='https://example.com',
            user=self.user
        )

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(f'/api/links/{link.id}/toggle_active/')
        assert response.status_code == 200
        assert response.data['is_active'] == False

    def test_user_can_view_stats(self):
        link = Link.objects.create(
            short_code='abc123',
            original_url='https://example.com',
            user=self.user
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/links/{link.id}/stats/')
        assert response.status_code == 200
        assert 'total_clicks' in response.data

    def test_check_link_status(self):
        link = Link.objects.create(
            short_code='abc123',
            original_url='https://example.com',
            is_active=True
        )

        response = self.client.get(f'/api/links/{link.id}/check_status/')
        assert response.status_code == 200
        assert response.data['is_active'] == True
