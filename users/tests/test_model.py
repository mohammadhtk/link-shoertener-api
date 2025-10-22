import pytest
from django.contrib.auth import get_user_model
from users.models import Role, Permission

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')

    def test_user_has_permission(self):
        role = Role.objects.create(name=Role.USER)
        permission = Permission.objects.create(
            name='Test Permission',
            code='test_permission'
        )
        role.permissions.add(permission)

        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=role
        )

        assert user.has_permission('test_permission')
        assert not user.has_permission('nonexistent_permission')

    def test_user_is_admin(self):
        admin_role = Role.objects.create(name=Role.ADMIN)
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role=admin_role
        )
        assert user.is_admin

    def test_guest_user_permissions(self):
        user = User.objects.create_user(
            username='guest',
            email='guest@example.com',
            password='guestpass123'
        )
        # Guest users can shorten links
        assert user.has_permission('shorten_link_random')
        assert user.has_permission('shorten_link_custom')


@pytest.mark.django_db
class TestRoleModel:
    def test_create_role(self):
        role = Role.objects.create(
            name=Role.USER,
            description='Test role'
        )
        assert role.name == Role.USER
        assert str(role) == Role.USER

    def test_role_has_permission(self):
        role = Role.objects.create(name=Role.USER)
        permission = Permission.objects.create(
            name='Edit Link',
            code='edit_link'
        )
        role.permissions.add(permission)

        assert role.has_permission('edit_link')
        assert not role.has_permission('nonexistent_permission')
