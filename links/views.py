from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Link
from .serializers import LinkSerializer, LinkCreateSerializer, LinkUpdateSerializer
from .services import LinkService
from .filters import LinkFilter
from users.permissions import (
    IsOwnerOrAdmin, IsAdmin, CanShortenLink,
    CanViewStats, CanManageAllLinks,
)
from analytics.services import AnalyticsService
from .schemas import (
    link_create_schema, link_list_schema, link_detail_schema,
    link_update_schema, link_delete_schema, link_stats_schema,
    link_toggle_active_schema, link_check_status_schema, user_links_schema
)


# Create a new short link (Guest, User, Admin)
class LinkCreateView(APIView):
    permission_classes = [CanShortenLink]

    @link_create_schema
    def post(self, request):
        serializer = LinkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user if request.user.is_authenticated else None
        note = serializer.validated_data.get('note', '')

        # Check note permission
        if note and (not user or not user.has_permission('add_note')):
            return Response(
                {'error': 'You do not have permission to add notes to links'},
                status=status.HTTP_403_FORBIDDEN
            )

        link = LinkService.create_link(
            original_url=serializer.validated_data['original_url'],
            user=user,
            custom_alias=serializer.validated_data.get('custom_alias'),
            note=note
        )

        return Response(
            LinkSerializer(link).data,
            status=status.HTTP_201_CREATED
        )


# List user's links (User, Admin)
class LinkListView(ListAPIView):
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LinkFilter
    search_fields = ['short_code', 'custom_alias', 'original_url', 'note']
    ordering_fields = ['created_at', 'updated_at', 'is_active']
    ordering = ['-created_at']

    @link_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.has_permission('manage_all_links'):
            return Link.objects.all()
        return Link.objects.filter(user=user)


# List links for a specific user (Admin only)
class UserLinksView(ListAPIView):
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LinkFilter
    ordering_fields = ['created_at', 'updated_at', 'is_active']
    ordering = ['-created_at']

    @user_links_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Link.objects.filter(user_id=user_id)


# Get, update, or delete link (Owner or Admin)
class LinkUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    @link_detail_schema
    def get(self, request, pk):
        try:
            link = Link.objects.get(pk=pk)
        except Link.DoesNotExist:
            return Response(
                {'error': 'Link not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check ownership
        if link.user != request.user and not request.user.has_permission('manage_all_links'):
            return Response(
                {'error': 'You do not have permission to view this link'},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(LinkSerializer(link).data)

    @link_update_schema
    def patch(self, request, pk):
        try:
            link = Link.objects.get(pk=pk)
        except Link.DoesNotExist:
            return Response(
                {'error': 'Link not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check ownership
        if link.user != request.user and not request.user.has_permission('manage_all_links'):
            return Response(
                {'error': 'You do not have permission to edit this link'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = LinkUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Check note permission
        if 'note' in serializer.validated_data and not request.user.has_permission('add_note'):
            return Response(
                {'error': 'You do not have permission to add/edit notes'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check active status permission
        if 'is_active' in serializer.validated_data and not request.user.has_permission('manage_all_links'):
            return Response(
                {'error': 'You do not have permission to activate/deactivate links'},
                status=status.HTTP_403_FORBIDDEN
            )

        link = LinkService.update_link(
            link=link,
            original_url=serializer.validated_data.get('original_url'),
            note=serializer.validated_data.get('note'),
            is_active=serializer.validated_data.get('is_active')
        )

        return Response(LinkSerializer(link).data)

    @link_delete_schema
    def delete(self, request, pk):
        # Check admin permission
        if not request.user.has_permission('manage_all_links'):
            return Response(
                {'error': 'You do not have permission to delete links'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            link = Link.objects.get(pk=pk)
        except Link.DoesNotExist:
            return Response(
                {'error': 'Link not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Get link statistics (Owner or Admin)
class LinkStatsView(APIView):
    permission_classes = [IsAuthenticated, CanViewStats, IsOwnerOrAdmin]

    @link_stats_schema
    def get(self, request, pk):
        try:
            link = Link.objects.get(pk=pk)
        except Link.DoesNotExist:
            return Response(
                {'error': 'Link not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check ownership
        if link.user != request.user and not request.user.has_permission('manage_all_links'):
            return Response(
                {'error': 'You do not have permission to view stats for this link'},
                status=status.HTTP_403_FORBIDDEN
            )

        stats = AnalyticsService.get_link_stats(link)
        return Response(stats)


# Toggle link active status (Admin only)
class LinkToggleActiveView(APIView):
    permission_classes = [IsAuthenticated, CanManageAllLinks]

    @link_toggle_active_schema
    def post(self, request, pk):
        try:
            link = Link.objects.get(pk=pk)
        except Link.DoesNotExist:
            return Response(
                {'error': 'Link not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        link.is_active = not link.is_active
        link.save()
        return Response(LinkSerializer(link).data)


# Check if link is active (Public)
class LinkCheckStatusView(APIView):
    permission_classes = [AllowAny]

    @link_check_status_schema
    def get(self, request, pk):
        try:
            link = Link.objects.get(pk=pk)
        except Link.DoesNotExist:
            return Response(
                {'error': 'Link not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            'short_code': link.short_code,
            'is_active': link.is_active
        })


# Redirect to original URL and track click (privacy-safe)
@extend_schema(exclude=True)
def redirect_link(request, code):
    link = LinkService.get_link_by_code(code)

    if not link:
        return Response({'error': 'Link not found'}, status=status.HTTP_404_NOT_FOUND)

    if not link.is_active:
        return Response({'error': 'Link is inactive'}, status=status.HTTP_410_GONE)

    # Track the click (privacy-safe - only timestamp)
    AnalyticsService.track_click(link=link)

    return redirect(link.original_url)
