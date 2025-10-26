from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import ClickStats


@admin.register(ClickStats)
class ClickStatsAdmin(admin.ModelAdmin):
    list_display = ['link_display', 'clicked_at_display', 'time_ago']
    list_filter = ['clicked_at', 'link']
    search_fields = ['link__short_code', 'link__custom_alias']
    readonly_fields = ['link', 'clicked_at']
    date_hierarchy = 'clicked_at'
    list_per_page = 50
    ordering = ['-clicked_at']

    def link_display(self, obj):
        """Display link with short code"""
        return format_html(
            '<a href="/admin/links/link/{}/change/">🔗 {}</a>',
            obj.link.id,
            obj.link.short_code or obj.link.custom_alias
        )

    link_display.short_description = 'Link'

    def clicked_at_display(self, obj):
        """Display formatted timestamp"""
        return format_html(
            '<span style="font-family: monospace; color: #495057;">📅 {}</span>',
            obj.clicked_at.strftime('%Y-%m-%d %H:%M:%S')
        )

    clicked_at_display.short_description = 'Clicked At'

    def time_ago(self, obj):
        """Display time ago"""
        from django.utils import timezone
        from datetime import timedelta

        now = timezone.now()
        diff = now - obj.clicked_at

        if diff < timedelta(minutes=1):
            return format_html('<span style="color: #28a745;">Just now</span>')
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return format_html('<span style="color: #28a745;">{} min ago</span>', minutes)
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return format_html('<span style="color: #ffc107;">{} hours ago</span>', hours)
        else:
            days = diff.days
            return format_html('<span style="color: #6c757d;">{} days ago</span>', days)

    time_ago.short_description = 'Time Ago'

    def has_add_permission(self, request):
        """Disable manual addition of click stats"""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing of click stats"""
        return False
