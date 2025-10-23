from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import ClickStatsSerializer


clickstats_list_schema = extend_schema(
    tags=['Analytics'],
    summary='List all click statistics',
    description='Retrieve a list of all click statistics. Admin permission required.',
    responses={
        200: OpenApiResponse(
            response=ClickStatsSerializer(many=True),
            description='List of click statistics'
        ),
        403: OpenApiResponse(description='Permission denied')
    }
)

clickstats_detail_schema = extend_schema(
    tags=['Analytics'],
    summary='Get click statistics details',
    description='Retrieve detailed information about a specific click statistic. Admin permission required.',
    responses={
        200: OpenApiResponse(
            response=ClickStatsSerializer,
            description='Click statistics details'
        ),
        403: OpenApiResponse(description='Permission denied'),
        404: OpenApiResponse(description='Click statistic not found')
    }
)

global_stats_schema = extend_schema(
    tags=['Analytics'],
    summary='Get global statistics',
    description='Retrieve global statistics including total links and total clicks. Admin permission required.',
    responses={
        200: OpenApiResponse(
            description='Global statistics',
            examples=[
                OpenApiExample(
                    'Global Stats Response',
                    value={
                        'total_links': 1250,
                        'total_clicks': 45678,
                        'active_links': 1100,
                        'inactive_links': 150
                    }
                )
            ]
        ),
        403: OpenApiResponse(description='Permission denied')
    }
)
