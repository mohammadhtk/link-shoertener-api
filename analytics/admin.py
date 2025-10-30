from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from .models import ClickStats


@admin.register(ClickStats)
class ClickStatsAdmin(admin.ModelAdmin):
    list_display = ['get_link', 'clicked_at', 'time_ago']
    list_filter = ['clicked_at', 'link']
    search_fields = ['link__short_code', 'link__custom_alias']
    readonly_fields = ['link', 'clicked_at']
    date_hierarchy = 'clicked_at'
    list_per_page = 50
    ordering = ['-clicked_at']

    def get_link(self, obj):
        """Display link with short code"""
        return obj.link.short_code or obj.link.custom_alias

    get_link.short_description = 'Link'
    get_link.admin_order_field = 'link__short_code'

    def time_ago(self, obj):
        """Display time ago"""
        now = timezone.now()
        diff = now - obj.clicked_at

        if diff < timedelta(minutes=1):
            return 'Just now'
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f'{minutes} min ago'
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f'{hours} hours ago'
        else:
            days = diff.days
            return f'{days} days ago'

    time_ago.short_description = 'Time Ago'

    def has_add_permission(self, request):
        """Disable manual addition of click stats"""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing of click stats"""
        return False
