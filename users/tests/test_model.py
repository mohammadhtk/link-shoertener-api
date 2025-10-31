import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        # Create a normal user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
        assert user.role == User.USER

    def test_user_is_admin(self):
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role=User.ADMIN
        )
        assert admin.is_admin
        assert not admin.is_guest
        assert admin.has_permission('any_permission')  # Admin should have all permissions

    def test_guest_permissions(self):
        guest = User.objects.create_user(
            username='guest',
            email='guest@example.com',
            password='guestpass123',
            role=User.GUEST
        )
        assert guest.is_guest
        assert guest.has_permission('shorten_link_random')
        assert guest.has_permission('shorten_link_custom')
        assert not guest.has_permission('edit_own_link')
        assert not guest.has_permission('nonexistent_permission')

    def test_user_permissions(self):
        user = User.objects.create_user(
            username='normal_user',
            email='normal@example.com',
            password='normalpass123',
            role=User.USER
        )
        assert user.has_permission('shorten_link_random')
        assert user.has_permission('add_note')
        assert not user.has_permission('admin_only_action')
