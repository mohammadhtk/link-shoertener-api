from django.contrib import admin
from .models import ClickStats


@admin.register(ClickStats)
class ClickStatsAdmin(admin.ModelAdmin):
    list_display = ['link', 'clicked_at']
    list_filter = ['clicked_at', 'link']
    search_fields = ['link__short_code']
    readonly_fields = ['link', 'clicked_at']
    date_hierarchy = 'clicked_at'
