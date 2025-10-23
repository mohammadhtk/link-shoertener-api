from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import ClickStats
from .serializers import ClickStatsSerializer
from .services import AnalyticsService
from users.permissions import IsAdmin
from .schemas import clickstats_list_schema, clickstats_detail_schema, global_stats_schema


# List all click statistics (Admin only)
class ClickStatsListView(ListAPIView):
    queryset = ClickStats.objects.all()
    serializer_class = ClickStatsSerializer
    permission_classes = [IsAdmin]



# Get click statistics details (Admin only)
class ClickStatsDetailView(RetrieveAPIView):
    queryset = ClickStats.objects.all()
    serializer_class = ClickStatsSerializer
    permission_classes = [IsAdmin]


# Get global statistics (Admin only)
class GlobalStatsView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(
        responses={200: OpenApiResponse(
            description='Global statistics',
            response={'total_links': 'integer', 'total_clicks': 'integer'}
        )}
    )
    def get(self, request):
        stats = AnalyticsService.get_global_stats()
        return Response(stats)
