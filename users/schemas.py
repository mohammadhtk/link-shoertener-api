from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    UserUpdateSerializer
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
                        'role': 'User'
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
                            'role': 'User'
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
        200: OpenApiResponse(response=UserSerializer, description='Current user information'),
        401: OpenApiResponse(description='Authentication required')
    }
)

user_list_schema = extend_schema(
    tags=['Users'],
    summary='List all users',
    description='Retrieve a list of all users. Admin permission required.',
    parameters=[
        OpenApiParameter(
            name='is_active',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Filter by active status'
        ),
        OpenApiParameter(
            name='role',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter by role (GUEST, USER, ADMIN)'
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
        200: OpenApiResponse(response=UserSerializer(many=True), description='List of users'),
        403: OpenApiResponse(description='Permission denied')
    }
)

user_detail_schema = extend_schema(
    tags=['Users'],
    summary='Get user details',
    description='Retrieve detailed information about a specific user. Admin permission required.',
    responses={
        200: OpenApiResponse(response=UserSerializer, description='User details'),
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
        200: OpenApiResponse(response=UserSerializer, description='User updated successfully'),
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
        200: OpenApiResponse(response=UserSerializer, description='User updated successfully'),
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
