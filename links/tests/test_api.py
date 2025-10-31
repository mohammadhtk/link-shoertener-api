import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from links.models import Link

User = get_user_model()


@pytest.mark.django_db
class TestLinkAPI:
    def setup_method(self):
        self.client = APIClient()

        # Setup users with simplified roles
        self.guest_user = User.objects.create_user(
            username='guest',
            email='guest@example.com',
            password='guestpass123',
            role=User.GUEST
        )

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=User.USER
        )

        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role=User.ADMIN
        )

    def test_guest_can_create_link(self):
        # Guest (unauthenticated) can create links
        data = {'original_url': 'https://example.com'}
        response = self.client.post('/api/links/', data)
        assert response.status_code == 201
        assert 'short_code' in response.data
        assert 'short_url' in response.data
        assert 'total_clicks' in response.data
        assert response.data['total_clicks'] == 0
        assert 'click_timestamps' in response.data
        assert response.data['click_timestamps'] == []

    def test_guest_can_create_link_with_custom_alias(self):
        data = {'original_url': 'https://example.com', 'custom_alias': 'mylink'}
        response = self.client.post('/api/links/', data)
        assert response.status_code == 201
        assert response.data['custom_alias'] == 'mylink'
        assert response.data['short_url'] == 'mylink'

    def test_guest_cannot_add_note(self):
        data = {'original_url': 'https://example.com', 'note': 'Note not allowed'}
        response = self.client.post('/api/links/', data)
        assert response.status_code == 403

    def test_user_can_add_note(self):
        self.client.force_authenticate(user=self.user)
        data = {'original_url': 'https://example.com', 'note': 'User note'}
        response = self.client.post('/api/links/', data)
        assert response.status_code == 201
        assert response.data['note'] == 'User note'

    def test_user_can_edit_own_link(self):
        self.client.force_authenticate(user=self.user)
        link = Link.objects.create(short_code='abc123', original_url='https://example.com', user=self.user)
        data = {'original_url': 'https://newurl.com', 'note': 'Updated note'}
        response = self.client.patch(f'/api/links/{link.id}/', data)
        assert response.status_code == 200
        assert response.data['original_url'] == 'https://newurl.com'
        assert response.data['note'] == 'Updated note'
        assert 'short_url' in response.data
        assert 'total_clicks' in response.data
        assert 'click_timestamps' in response.data

    def test_user_cannot_edit_others_link(self):
        other_user = User.objects.create_user(username='other', email='other@example.com', password='pass123', role=User.USER)
        link = Link.objects.create(short_code='xyz123', original_url='https://example.com', user=other_user)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/api/links/{link.id}/', {'original_url': 'https://newurl.com'})
        assert response.status_code == 403

    def test_admin_can_edit_any_link(self):
        link = Link.objects.create(short_code='abc123', original_url='https://example.com', user=self.user)
        self.client.force_authenticate(user=self.admin)
        data = {'original_url': 'https://newurl.com', 'note': 'Admin edit'}
        response = self.client.patch(f'/api/links/{link.id}/', data)
        assert response.status_code == 200
        assert response.data['original_url'] == 'https://newurl.com'
        assert response.data['note'] == 'Admin edit'

    def test_admin_can_toggle_link_status(self):
        link = Link.objects.create(short_code='abc123', original_url='https://example.com', user=self.user)
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(f'/api/links/{link.id}/toggle_active/')
        assert response.status_code == 200
        assert response.data['is_active'] == False

    def test_user_can_view_stats(self):
        link = Link.objects.create(short_code='abc123', original_url='https://example.com', user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/links/{link.id}/stats/')
        assert response.status_code == 200
        assert 'total_clicks' in response.data
        assert 'daily_clicks' in response.data

    def test_check_link_status(self):
        link = Link.objects.create(short_code='abc123', original_url='https://example.com', is_active=True)
        response = self.client.get(f'/api/links/{link.id}/check_status/')
        assert response.status_code == 200
        assert response.data['is_active'] is True
