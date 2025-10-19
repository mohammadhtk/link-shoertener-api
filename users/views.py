from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .models import User, Role, Permission
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    UserUpdateSerializer, RoleSerializer, PermissionSerializer,
    LoginResponseSerializer
)
from .services import UserService
from .permissions import IsAdmin, CanManageUsers

# Register a new user
class UserRegisterView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={201: UserSerializer}
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

# Login user and get JWT tokens
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserLoginSerializer,
        responses={
            200: OpenApiResponse(
                response=LoginResponseSerializer,  # or OpenApiTypes.OBJECT if you don’t want a serializer
                description='Login successful'
            )
        }
    )
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

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# List all users (Admin only)
class UserListView(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]


# Get user details (Admin only)
class UserDetailView(RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]

# Update user (admin only)
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]

    @extend_schema(request=UserUpdateSerializer, responses={200: UserSerializer})
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(request=UserUpdateSerializer, responses={200: UserSerializer})
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        user = self.get_object()
        user = UserService.update_user(user, **serializer.validated_data)
        return user

# Delete user (Admin only)
class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]


# List all roles
class RoleListView(ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


# Get role details
class RoleDetailView(RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


# Get all permissions for a specific role
class RolePermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: PermissionSerializer(many=True)})
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


# Get permission details (Admin only)
class PermissionDetailView(RetrieveAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
