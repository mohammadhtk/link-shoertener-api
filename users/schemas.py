from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    UserUpdateSerializer, RoleSerializer, PermissionSerializer
)

# Authentication Schemas
user_register_schema = extend_schema(
    tags=['Authentication'],
    summary='Register a new user',
    description='Create a new user account. By default, users are assigned the "User" role.',
    request=UserRegistrationSerializer,
    responses={
        201: OpenApiResponse(
            response=UserSerializer,
            description='User successfully registered',
            examples=[
                OpenApiExample(
                    'Success Response',
                    value={
                        'id': 1,
                        'username': 'john_doe',
                        'email': 'john@example.com',
                        'role': {'id': 2, 'name': 'User'}
                    }
                )
            ]
        ),
        400: OpenApiResponse(description='Invalid input data')
    },
    examples=[
        OpenApiExample(
            'Registration Request',
            value={
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'SecurePass123!'
            },
            request_only=True
        )
    ]
)

user_login_schema = extend_schema(
    tags=['Authentication'],
    summary='User login',
    description='Authenticate user and receive JWT access and refresh tokens.',
    request=UserLoginSerializer,
    responses={
        200: OpenApiResponse(
            description='Login successful',
            examples=[
                OpenApiExample(
                    'Success Response',
                    value={
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                        'user': {
                            'id': 1,
                            'username': 'john_doe',
                            'email': 'john@example.com',
                            'role': {'id': 2, 'name': 'User'}
                        }
                    }
                )
            ]
        ),
        401: OpenApiResponse(description='Invalid credentials')
    },
    examples=[
        OpenApiExample(
            'Login Request',
            value={
                'username': 'john_doe',
                'password': 'SecurePass123!'
            },
            request_only=True
        )
    ]
)

# User Schemas
user_me_schema = extend_schema(
    tags=['Users'],
    summary='Get current user',
    description='Retrieve the currently authenticated user\'s information.',
    responses={
        200: OpenApiResponse(
            response=UserSerializer,
            description='Current user information'
        ),
        401: OpenApiResponse(description='Authentication required')
    }
)

user_list_schema = extend_schema(
    tags=['Users'],
    summary='List all users',
    description='''
    Retrieve a list of all users with filtering and search capabilities. Admin permission required.

    **Filtering:**
    - `is_active`: Filter by active status (true/false)
    - `role__name`: Filter by role name (Guest, User, Admin)

    **Search:**
    - Search by username or email

    **Ordering:**
    - Order by username, email, or created_at
    - Use `-` prefix for descending order (e.g., `-created_at`)
    ''',
    parameters=[
        OpenApiParameter(
            name='is_active',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Filter by active status'
        ),
        OpenApiParameter(
            name='role__name',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter by role name (Guest, User, Admin)'
        ),
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Search by username or email'
        ),
        OpenApiParameter(
            name='ordering',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Order by field (username, email, created_at). Use - for descending.'
        ),
        OpenApiParameter(
            name='page',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Page number for pagination'
        ),
        OpenApiParameter(
            name='page_size',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Number of items per page'
        )
    ],
    responses={
        200: OpenApiResponse(
            response=UserSerializer(many=True),
            description='List of users'
        ),
        403: OpenApiResponse(description='Permission denied')
    }
)

user_detail_schema = extend_schema(
    tags=['Users'],
    summary='Get user details',
    description='Retrieve detailed information about a specific user. Admin permission required.',
    responses={
        200: OpenApiResponse(
            response=UserSerializer,
            description='User details'
        ),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='User not found')
    }
)

user_update_put_schema = extend_schema(
    tags=['Users'],
    summary='Update user (full)',
    description='Update all fields of a user. Admin permission required.',
    request=UserUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=UserSerializer,
            description='User updated successfully'
        ),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='User not found')
    }
)

user_update_patch_schema = extend_schema(
    tags=['Users'],
    summary='Update user (partial)',
    description='Update specific fields of a user. Admin permission required.',
    request=UserUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=UserSerializer,
            description='User updated successfully'
        ),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='User not found')
    }
)

user_delete_schema = extend_schema(
    tags=['Users'],
    summary='Delete user',
    description='Delete a user account. Admin permission required.',
    responses={
        204: OpenApiResponse(description='User deleted successfully'),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='User not found')
    }
)

# Role Schemas
role_list_schema = extend_schema(
    tags=['Roles & Permissions'],
    summary='List all roles',
    description='Retrieve a list of all available roles in the system.',
    responses={
        200: OpenApiResponse(
            response=RoleSerializer(many=True),
            description='List of roles'
        )
    }
)

role_detail_schema = extend_schema(
    tags=['Roles & Permissions'],
    summary='Get role details',
    description='Retrieve detailed information about a specific role.',
    responses={
        200: OpenApiResponse(
            response=RoleSerializer,
            description='Role details'
        ),
        404: OpenApiResponse(description='Role not found')
    }
)

role_permissions_schema = extend_schema(
    tags=['Roles & Permissions'],
    summary='Get role permissions',
    description='Retrieve all permissions assigned to a specific role.',
    responses={
        200: OpenApiResponse(
            response=PermissionSerializer(many=True),
            description='List of permissions for the role'
        ),
        404: OpenApiResponse(description='Role not found')
    }
)

# Permission Schemas
permission_list_schema = extend_schema(
    tags=['Roles & Permissions'],
    summary='List all permissions',
    description='Retrieve a list of all available permissions. Admin permission required.',
    responses={
        200: OpenApiResponse(
            response=PermissionSerializer(many=True),
            description='List of permissions'
        ),
        403: OpenApiResponse(description='Permission denied')
    }
)

permission_detail_schema = extend_schema(
    tags=['Roles & Permissions'],
    summary='Get permission details',
    description='Retrieve detailed information about a specific permission. Admin permission required.',
    responses={
        200: OpenApiResponse(
            response=PermissionSerializer,
            description='Permission details'
        ),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Permission not found')
    }
)
