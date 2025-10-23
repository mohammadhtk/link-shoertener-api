from django.urls import path
from .views import (
    LinkCreateView, LinkListView, LinkDetailView, LinkUpdateView, LinkDeleteView,
    LinkStatsView, LinkToggleActiveView, LinkCheckStatusView, redirect_link,
    UserLinksView
)

api_urlpatterns = [
    path('', LinkCreateView.as_view(), name='link-create'),
    path('list/', LinkListView.as_view(), name='link-list'),
    path('user/<int:user_id>/', UserLinksView.as_view(), name='user-links'),
    path('<int:pk>/', LinkDetailView.as_view(), name='link-detail'),
    path('<int:pk>/update/', LinkUpdateView.as_view(), name='link-update'),
    path('<int:pk>/delete/', LinkDeleteView.as_view(), name='link-delete'),
    path('<int:pk>/stats/', LinkStatsView.as_view(), name='link-stats'),
    path('<int:pk>/toggle-active/', LinkToggleActiveView.as_view(), name='link-toggle-active'),
    path('<int:pk>/check-status/', LinkCheckStatusView.as_view(), name='link-check-status'),
]

redirect_urlpatterns = [
    path('<str:code>/', redirect_link, name='redirect'),
]

urlpatterns = api_urlpatterns + redirect_urlpatterns
