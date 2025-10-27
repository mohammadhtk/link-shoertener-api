from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Role, Permission
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    UserUpdateSerializer, RoleSerializer, PermissionSerializer
)
from .services import UserService
from .permissions import IsAdmin, CanManageUsers
from .schemas import (
    user_register_schema, user_login_schema, user_me_schema,
    user_list_schema, user_detail_schema, user_update_put_schema,
    user_update_patch_schema, user_delete_schema, role_list_schema,
    role_detail_schema, role_permissions_schema, permission_list_schema,
    permission_detail_schema
)

# Register a new user
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    @user_register_schema
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        tokens = UserService.generate_tokens(user)

        return Response(
            {
                'access': tokens['access'],
                'refresh': tokens['refresh'],
                'user': UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )


# Login user and get JWT tokens
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    @user_login_schema
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = UserService.authenticate_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if not result:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({
            'access': result['access'],
            'refresh': result['refresh'],
            'user': UserSerializer(result['user']).data
        })


# Get current authenticated user
class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    @user_me_schema
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# List all users (Admin only)
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'role__name']
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email', 'created_at']
    ordering = ['-created_at']

    @user_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# Get, update, or delete user (Admin only)
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, CanManageUsers]

    @user_detail_schema
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(UserSerializer(user).data)

    @user_update_patch_schema
    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = UserService.update_user(user, **serializer.validated_data)
        return Response(UserSerializer(user).data)

    @user_update_put_schema
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.update_user(user, **serializer.validated_data)
        return Response(UserSerializer(user).data)

    @user_delete_schema
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# List all roles
class RoleListView(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    @role_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# Get role details
class RoleDetailView(RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    @role_detail_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# Get all permissions for a specific role
class RolePermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    @role_permissions_schema
    def get(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response(
                {'error': 'Role not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PermissionSerializer(role.permissions.all(), many=True)
        return Response(serializer.data)

# List all permissions (Admin only)
class PermissionListView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    @permission_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# Get permission details (Admin only)
class PermissionDetailView(RetrieveAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    @permission_detail_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
