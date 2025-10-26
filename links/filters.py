import django_filters
from django.db import models
from .models import Link


class LinkFilter(django_filters.FilterSet):
    """Filter for Link model"""
    is_active = django_filters.BooleanFilter(field_name='is_active')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    has_custom_alias = django_filters.BooleanFilter(method='filter_has_custom_alias')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Link
        fields = ['is_active', 'created_after', 'created_before']

    def filter_has_custom_alias(self, queryset, name, value):
        """Filter links that have custom aliases"""
        if value:
            return queryset.exclude(custom_alias__isnull=True).exclude(custom_alias='')
        return queryset.filter(custom_alias__isnull=True) | queryset.filter(custom_alias='')

    def filter_search(self, queryset, name, value):
        """Search in short_code, custom_alias, original_url, and note"""
        return queryset.filter(
            models.Q(short_code__icontains=value) |
            models.Q(custom_alias__icontains=value) |
            models.Q(original_url__icontains=value) |
            models.Q(note__icontains=value)
        )
