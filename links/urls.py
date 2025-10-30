from django.urls import path
from .views import (
    LinkCreateView, LinkListView, LinkUpdateView,
    LinkStatsView, LinkToggleActiveView, LinkCheckStatusView, RedirectLinkView,
    UserLinksView
)

api_urlpatterns = [
    path('', LinkCreateView.as_view(), name='link-create'),
    path('list/', LinkListView.as_view(), name='link-list'),
    path('user/<int:user_id>/', UserLinksView.as_view(), name='user-links'),
    path('<int:pk>/', LinkUpdateView.as_view(), name='link-detail-update'),
    path('<int:pk>/stats/', LinkStatsView.as_view(), name='link-stats'),
    path('<int:pk>/toggle_active/', LinkToggleActiveView.as_view(), name='link-toggle-active'),
    path('<int:pk>/check_status/', LinkCheckStatusView.as_view(), name='link-check-status'),
]

redirect_urlpatterns = [
    path('<str:code>/', RedirectLinkView.as_view(), name='redirect'),
]

urlpatterns = api_urlpatterns + redirect_urlpatterns
