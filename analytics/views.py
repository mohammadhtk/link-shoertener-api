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

    @clickstats_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# Get click statistics details (Admin only)
class ClickStatsDetailView(RetrieveAPIView):
    queryset = ClickStats.objects.all()
    serializer_class = ClickStatsSerializer
    permission_classes = [IsAdmin]

    @clickstats_detail_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# Get global statistics (Admin only)
class GlobalStatsView(APIView):
    permission_classes = [IsAdmin]

    @global_stats_schema
    def get(self, request):
        stats = AnalyticsService.get_global_stats()
        return Response(stats)
