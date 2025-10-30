from django.contrib import admin
from django.utils.html import format_html
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['short_code', 'custom_alias', 'original_url_truncated', 'user', 'is_active', 'total_clicks',
                    'created_at']
    list_filter = ['is_active', 'created_at', 'user']
    search_fields = ['short_code', 'custom_alias', 'original_url', 'user__username', 'note']
    readonly_fields = ['short_code', 'total_clicks', 'created_at', 'updated_at']
    fieldsets = (
        ('Link Information', {
            'fields': ('short_code', 'custom_alias', 'original_url', 'user')
        }),
        ('Status & Analytics', {
            'fields': ('is_active', 'total_clicks')
        }),
        ('Additional Information', {
            'fields': ('note', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 25
    date_hierarchy = 'created_at'
    actions = ['activate_links', 'deactivate_links']

    def original_url_truncated(self, obj):
        """Display truncated URL with link"""
        url = obj.original_url
        if len(url) > 50:
            url = url[:47] + '...'
        return format_html('<a href="{}" target="_blank">{}</a>', obj.original_url, url)

    original_url_truncated.short_description = 'Original URL'

    def total_clicks(self, obj):
        """Display total clicks"""
        return obj.total_clicks

    total_clicks.short_description = 'Clicks'

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
