from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['short_code_display', 'custom_alias', 'original_url_display', 'user', 'status_badge',
                    'total_clicks', 'created_at']
    list_filter = ['is_active', 'created_at', 'user']
    search_fields = ['short_code', 'custom_alias', 'original_url', 'user__username', 'note']
    readonly_fields = ['short_code', 'total_clicks', 'created_at', 'updated_at', 'click_chart']
    fieldsets = (
        ('Link Information', {
            'fields': ('short_code', 'custom_alias', 'original_url', 'user')
        }),
        ('Status & Analytics', {
            'fields': ('is_active', 'total_clicks', 'click_chart')
        }),
        ('Additional Information', {
            'fields': ('note', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 25
    date_hierarchy = 'created_at'
    actions = ['activate_links', 'deactivate_links']

    def short_code_display(self, obj):
        """Display short code with copy button"""
        return format_html(
            '<code style="background: #f5f5f5; padding: 4px 8px; border-radius: 4px;">{}</code>',
            obj.short_code
        )

    short_code_display.short_description = 'Short Code'

    def original_url_display(self, obj):
        """Display truncated URL with link"""
        url = obj.original_url
        if len(url) > 50:
            url = url[:47] + '...'
        return format_html('<a href="{}" target="_blank">{}</a>', obj.original_url, url)

    original_url_display.short_description = 'Original URL'

    def status_badge(self, obj):
        """Display status as colored badge"""
        if obj.is_active:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">Active</span>'
            )
        return format_html(
            '<span style="background: #dc3545; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">Inactive</span>'
        )

    status_badge.short_description = 'Status'

    def total_clicks(self, obj):
        """Display total clicks with icon"""
        count = obj.total_clicks
        return format_html(
            '<span style="font-weight: bold; color: #007bff;">📊 {}</span>',
            count
        )

    total_clicks.short_description = 'Total Clicks'

    def click_chart(self, obj):
        """Display simple click chart"""
        from analytics.models import ClickStats
        from django.utils import timezone
        from datetime import timedelta

        # Get last 7 days of clicks
        seven_days_ago = timezone.now() - timedelta(days=7)
        daily_clicks = ClickStats.objects.filter(
            link=obj,
            clicked_at__gte=seven_days_ago
        ).extra(
            select={'day': 'DATE(clicked_at)'}
        ).values('day').annotate(count=Count('id')).order_by('day')

        # Create simple bar chart
        chart_html = '<div style="display: flex; align-items: flex-end; gap: 4px; height: 60px;">'
        max_clicks = max([d['count'] for d in daily_clicks], default=1)

        for day_data in daily_clicks:
            height = (day_data['count'] / max_clicks) * 50
            chart_html += f'''
                <div style="
                    width: 30px;
                    height: {height}px;
                    background: #007bff;
                    border-radius: 2px;
                    position: relative;
                " title="{day_data['day']}: {day_data['count']} clicks">
                    <span style="
                        position: absolute;
                        top: -20px;
                        left: 50%;
                        transform: translateX(-50%);
                        font-size: 10px;
                    ">{day_data['count']}</span>
                </div>
            '''

        chart_html += '</div>'
        chart_html += '<p style="margin-top: 10px; font-size: 12px; color: #666;">Last 7 days click activity</p>'

        return format_html(chart_html)

    click_chart.short_description = 'Click Activity'

    def activate_links(self, request, queryset):
        """Bulk activate links"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} link(s) activated successfully.')

    activate_links.short_description = 'Activate selected links'

    def deactivate_links(self, request, queryset):
        """Bulk deactivate links"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} link(s) deactivated successfully.')

    deactivate_links.short_description = 'Deactivate selected links'
