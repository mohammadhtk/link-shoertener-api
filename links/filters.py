import django_filters
from django.db.models import Q
from .models import Link

class LinkFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='is_active')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    has_custom_alias = django_filters.BooleanFilter(method='filter_has_custom_alias')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Link
        fields = ['is_active', 'created_after', 'created_before']

    def filter_has_custom_alias(self, queryset, name, value):
        if value:
            return queryset.exclude(Q(custom_alias__isnull=True) | Q(custom_alias=''))
        return queryset.filter(Q(custom_alias__isnull=True) | Q(custom_alias=''))

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(short_code__icontains=value) |
            Q(custom_alias__icontains=value) |
            Q(original_url__icontains=value) |
            Q(note__icontains=value)
        )
