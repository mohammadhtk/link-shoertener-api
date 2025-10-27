from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Role, Permission


class UserService:

    # Create a new user with specified role (default: User)
    @staticmethod
    def create_user(username, email, password, role_name=Role.USER):
        role = Role.objects.filter(name=role_name).first()

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
            role_name = kwargs.pop('role')
            role = Role.objects.filter(name=role_name).first()
            if role:
                user.role = role

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.save()
        return user


class RoleService:

    # Setup default roles and permissions
    @staticmethod
    def setup_default_roles():
        # Define all permissions
        permissions_data = [
            # Guest permissions
            {'code': 'shorten_link_random', 'name': 'Shorten Link (Random)',
             'description': 'Can shorten links with random code'},
            {'code': 'shorten_link_custom', 'name': 'Shorten Link (Custom)',
             'description': 'Can shorten links with custom alias'},

            # User permissions
            {'code': 'add_note', 'name': 'Add Note', 'description': 'Can add notes to links'},
            {'code': 'edit_link', 'name': 'Edit Link', 'description': 'Can edit destination URL'},
            {'code': 'view_stats', 'name': 'View Statistics', 'description': 'Can view click statistics'},

            # Admin permissions
            {'code': 'manage_all_links', 'name': 'Manage All Links',
             'description': 'Can view, edit, activate/deactivate, or delete any link'},
            {'code': 'manage_users', 'name': 'Manage Users', 'description': 'Can create, edit, delete users'},
            {'code': 'access_dashboard', 'name': 'Access Dashboard',
             'description': 'Can access dashboard and system settings'},
        ]

        # Create permissions
        permissions = {}
        for perm_data in permissions_data:
            perm, created = Permission.objects.get_or_create(
                code=perm_data['code'],
                defaults={
                    'name': perm_data['name'],
                    'description': perm_data['description']
                }
            )
            permissions[perm_data['code']] = perm

        # Create Guest role
        guest_role, created = Role.objects.get_or_create(
            name=Role.GUEST,
            defaults={'description': 'Guest user with basic link shortening capabilities'}
        )
        guest_role.permissions.set([
            permissions['shorten_link_random'],
            permissions['shorten_link_custom'],
        ])

        # Create User role
        user_role, created = Role.objects.get_or_create(
            name=Role.USER,
            defaults={'description': 'Regular user with full link management capabilities'}
        )
        user_role.permissions.set([
            permissions['shorten_link_random'],
            permissions['shorten_link_custom'],
            permissions['add_note'],
            permissions['edit_link'],
            permissions['view_stats'],
        ])

        # Create Admin role
        admin_role, created = Role.objects.get_or_create(
            name=Role.ADMIN,
            defaults={'description': 'Administrator with full system access'}
        )
        admin_role.permissions.set([
            permissions['shorten_link_random'],
            permissions['shorten_link_custom'],
            permissions['add_note'],
            permissions['edit_link'],
            permissions['view_stats'],
            permissions['manage_all_links'],
            permissions['manage_users'],
            permissions['access_dashboard'],
        ])

        return {
            'guest': guest_role,
            'user': user_role,
            'admin': admin_role,
        }
