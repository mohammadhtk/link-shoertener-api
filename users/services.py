from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserService:

    # Create a new user with a role (default: USER)
    @staticmethod
    def create_user(username, email, password, role=User.USER):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        return user

    # Authenticate user and return JWT tokens
    @staticmethod
    def authenticate_user(username, password):
        user = authenticate(username=username, password=password)
        if not user:
            return None

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    # Generate JWT tokens for a user
    @staticmethod
    def generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    # Update user fields
    @staticmethod
    def update_user(user, **kwargs):
        if 'role' in kwargs:
            role_value = kwargs.pop('role')
            if role_value in [User.GUEST, User.USER, User.ADMIN]:
                user.role = role_value

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.save()
        return user


class RoleService:

    # Hard-coded permissions mapping for each role
    ROLE_PERMISSIONS = {
        User.GUEST: ['shorten_link_random', 'shorten_link_custom'],
        User.USER: [
            'shorten_link_random',
            'shorten_link_custom',
            'add_note',
            'edit_own_link',
            'view_own_stats'
        ],
        User.ADMIN: [
            'shorten_link_random',
            'shorten_link_custom',
            'add_note',
            'edit_own_link',
            'view_own_stats',
            'manage_all_links',
            'manage_users',
            'access_dashboard'
        ],
    }

    # Return list of permission codes for a role
    @staticmethod
    def get_permissions_for_role(role):
        return RoleService.ROLE_PERMISSIONS.get(role, [])
