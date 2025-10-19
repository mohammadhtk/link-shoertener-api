from rest_framework import permissions


class IsGuest(permissions.BasePermission):
    """Permission class to check if user is Guest (unauthenticated)"""

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsUser(permissions.BasePermission):
    """Permission class to check if user has User role"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role and request.user.role.name == 'User'


class IsAdmin(permissions.BasePermission):
    """Permission class to check if user is Admin"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsUserOrAdmin(permissions.BasePermission):
    """Permission class to check if user has User or Admin role"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role and request.user.role.name in ['User', 'Admin']


class IsGuestOrUser(permissions.BasePermission):
    """Permission class to check if user is Guest or has User role"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True  # Guest
        return request.user.role and request.user.role.name in ['User', 'Admin']


class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission class to check if user is owner or admin"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_admin:
            return True
        return obj.user == request.user


class HasPermission(permissions.BasePermission):
    """
    Custom permission class to check if user has specific permission.
    Usage: Set permission_required attribute on the view.
    """

    def has_permission(self, request, view):
        permission_code = getattr(view, 'permission_required', None)
        if not permission_code:
            return True

        # Guest users (unauthenticated)
        if not request.user.is_authenticated:
            return permission_code in ['shorten_link_random', 'shorten_link_custom']

        return request.user.has_permission(permission_code)

# Permission to shorten links (Guest, User, Admin)
class CanShortenLink(permissions.BasePermission):

    def has_permission(self, request, view):
        # All users including guests can shorten links
        return True

# Permission to add notes to links (User, Admin)
class CanAddNote(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_permission('add_note')

# Permission to edit links (User, Admin)
class CanEditLink(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_permission('edit_link')

# Permission to view click statistics (User, Admin)
class CanViewStats(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_permission('view_stats')

# Permission to manage all links (Admin only)
class CanManageAllLinks(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_permission('manage_all_links')

# Permission to manage users (Admin only)
class CanManageUsers(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_permission('manage_users')

