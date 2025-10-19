from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegisterView, UserLoginView, UserMeView,
    UserListView, UserDetailView, UserUpdateView, UserDeleteView,
    RoleListView, RoleDetailView, RolePermissionsView,
    PermissionListView, PermissionDetailView
)

urlpatterns = [
    # Authentication
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', UserMeView.as_view(), name='user-me'),

    # User management
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),

    # Roles
    path('roles/', RoleListView.as_view(), name='role-list'),
    path('roles/<int:pk>/', RoleDetailView.as_view(), name='role-detail'),
    path('roles/<int:pk>/permissions/', RolePermissionsView.as_view(), name='role-permissions'),

    # Permissions
    path('permissions/', PermissionListView.as_view(), name='permission-list'),
    path('permissions/<int:pk>/', PermissionDetailView.as_view(), name='permission-detail'),
]
