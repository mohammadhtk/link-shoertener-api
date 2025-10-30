from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'description']
    search_fields = ['name', 'code']
    ordering = ['name']
    list_per_page = 25


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'permission_count', 'user_count']
    search_fields = ['name']
    filter_horizontal = ['permissions']
    ordering = ['name']
    list_per_page = 25

    def permission_count(self, obj):
        """Display permission count"""
        return obj.permissions.count()

    permission_count.short_description = 'Permissions'

    def user_count(self, obj):
        """Display user count"""
        return User.objects.filter(role=obj).count()

    user_count.short_description = 'Users'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'get_role', 'is_active', 'link_count', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    list_per_page = 25

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Permissions', {'fields': ('role',)}),
        ('Important Dates', {'fields': ('created_at',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Permissions', {'fields': ('role',)}),
    )
    readonly_fields = ['created_at']

    def get_role(self, obj):
        """Display role name"""
        return obj.role.name if obj.role else 'No Role'

    get_role.short_description = 'Role'
    get_role.admin_order_field = 'role__name'

    def link_count(self, obj):
        """Display link count"""
        from links.models import Link
        return Link.objects.filter(user=obj).count()

    link_count.short_description = 'Links'
