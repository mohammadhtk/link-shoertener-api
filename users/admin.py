from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Displayed fields in list view
    list_display = ['username', 'email', 'role', 'is_active', 'link_count', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    list_per_page = 25

    # Customize field layout
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Permissions', {'fields': ('role',)}),
        ('Important Dates', {'fields': ('created_at',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Permissions', {'fields': ('role',)}),
    )

    readonly_fields = ['created_at']

    # Count number of links created by user
    def link_count(self, obj):
        from links.models import Link
        return Link.objects.filter(user=obj).count()

    link_count.short_description = 'Links'
