from django.contrib import admin
from .models import Link

# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['short_code', 'custom_alias', 'original_url', 'user', 'is_active', 'total_clicks', 'created_at']
    list_filter = ['is_active', 'created_at', 'user']
    search_fields = ['short_code', 'custom_alias', 'original_url', 'user__username']
    readonly_fields = ['short_code', 'total_clicks', 'created_at', 'updated_at']

    def total_clicks(self, obj):
        return obj.total_clicks

    total_clicks.short_description = 'Total Clicks'
