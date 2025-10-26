from django.urls import path
from .views import ClickStatsListView, ClickStatsDetailView, GlobalStatsView, ClickChartDataView

urlpatterns = [
    path('clicks/', ClickStatsListView.as_view(), name='clickstats-list'),
    path('clicks/<int:pk>/', ClickStatsDetailView.as_view(), name='clickstats-detail'),
    path('global-stats/', GlobalStatsView.as_view(), name='global-stats'),
    path('chart-data/', ClickChartDataView.as_view(), name='chart-data'),
]
