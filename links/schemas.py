from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializers import LinkSerializer, LinkCreateSerializer, LinkUpdateSerializer


link_create_schema = extend_schema(
    tags=['Links'],
    summary='Create a short link',
    description='Create a new shortened link. Guests can create links with random or custom aliases. Users can also add notes.',
    request=LinkCreateSerializer,
    responses={
        201: OpenApiResponse(
            response=LinkSerializer,
            description='Link created successfully',
            examples=[
                OpenApiExample(
                    'Success Response',
                    value={
                        'id': 1,
                        'short_code': 'abc123',
                        'original_url': 'https://example.com',
                        'custom_alias': None,
                        'note': '',
                        'is_active': True,
                        'created_at': '2024-01-01T12:00:00Z'
                    }
                )
            ]
        ),
        403: OpenApiResponse(description='Permission denied')
    },
    examples=[
        OpenApiExample(
            'Random Short Code',
            value={
                'original_url': 'https://example.com'
            },
            request_only=True
        ),
        OpenApiExample(
            'Custom Alias',
            value={
                'original_url': 'https://example.com',
                'custom_alias': 'my-link'
            },
            request_only=True
        ),
        OpenApiExample(
            'With Note (User only)',
            value={
                'original_url': 'https://example.com',
                'note': 'My important link'
            },
            request_only=True
        )
    ]
)

link_list_schema = extend_schema(
    tags=['Links'],
    summary='List links',
    description='List all links. Users see their own links, Admins see all links.',
    responses={
        200: OpenApiResponse(
            response=LinkSerializer(many=True),
            description='List of links'
        ),
        401: OpenApiResponse(description='Authentication required')
    }
)

link_detail_schema = extend_schema(
    tags=['Links'],
    summary='Get link details',
    description='Retrieve detailed information about a specific link. Must be owner or admin.',
    responses={
        200: OpenApiResponse(
            response=LinkSerializer,
            description='Link details'
        ),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Link not found')
    }
)

link_update_schema = extend_schema(
    tags=['Links'],
    summary='Update link',
    description='Update link details. Users can edit their own links, Admins can edit any link.',
    request=LinkUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=LinkSerializer,
            description='Link updated successfully'
        ),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Link not found')
    },
    examples=[
        OpenApiExample(
            'Update URL',
            value={'original_url': 'https://newurl.com'},
            request_only=True
        ),
        OpenApiExample(
            'Update Note',
            value={'note': 'Updated note'},
            request_only=True
        ),
        OpenApiExample(
            'Deactivate Link (Admin only)',
            value={'is_active': False},
            request_only=True
        )
    ]
)

link_delete_schema = extend_schema(
    tags=['Links'],
    summary='Delete link',
    description='Delete a link. Admin permission required.',
    responses={
        204: OpenApiResponse(description='Link deleted successfully'),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Link not found')
    }
)

link_stats_schema = extend_schema(
    tags=['Links'],
    summary='Get link statistics',
    description='Retrieve click statistics for a specific link. Must be owner or admin.',
    responses={
        200: OpenApiResponse(
            description='Link statistics',
            examples=[
                OpenApiExample(
                    'Statistics Response',
                    value={
                        'total_clicks': 150,
                        'daily_clicks': [
                            {'date': '2024-01-01', 'clicks': 10},
                            {'date': '2024-01-02', 'clicks': 15}
                        ]
                    }
                )
            ]
        ),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Link not found')
    }
)

link_toggle_active_schema = extend_schema(
    tags=['Links'],
    summary='Toggle link active status',
    description='Activate or deactivate a link. Admin permission required.',
    responses={
        200: OpenApiResponse(
            response=LinkSerializer,
            description='Link status toggled successfully'
        ),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Link not found')
    }
)

link_check_status_schema = extend_schema(
    tags=['Links'],
    summary='Check link status',
    description='Check if a link is active. Public endpoint.',
    responses={
        200: OpenApiResponse(
            description='Link status',
            examples=[
                OpenApiExample(
                    'Active Link',
                    value={
                        'short_code': 'abc123',
                        'is_active': True
                    }
                )
            ]
        ),
        404: OpenApiResponse(description='Link not found')
    }
)

user_links_schema = extend_schema(
    tags=['Links'],
    summary='List links for a specific user',
    description='Retrieve all links created by a specific user. Admin permission required.',
    parameters=[
        OpenApiParameter(
            name='user_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='User ID'
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
            response=LinkSerializer(many=True),
            description='List of user links'
        ),
        403: OpenApiResponse(description='Permission denied - Admin only'),
        404: OpenApiResponse(description='User not found')
    }
)
