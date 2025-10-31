from rest_framework import permissions

# Check if user is a Guest (unauthenticated)
class IsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated

# Check if user has role USER
class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'USER'

# Check if user has role ADMIN
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

# Check if user is USER or ADMIN
class IsUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['USER', 'ADMIN']

# Check if user is GUEST or USER
class IsGuestOrUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Guests are allowed, authenticated users must be USER or ADMIN
        if not request.user.is_authenticated:
            return True
        return request.user.role in ['USER', 'ADMIN']

# Check if user is owner of object or ADMIN
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin can access anything, otherwise only the owner
        return request.user.is_authenticated and (request.user.role == 'ADMIN' or getattr(obj, 'user', None) == request.user)

# Generic simplified permission system using permission codes
class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        permission_code = getattr(view, 'permission_required', None)
        if not permission_code:
            return True

        guest_permissions = ['shorten_link_random', 'shorten_link_custom']
        if not request.user.is_authenticated:
            return permission_code in guest_permissions

        if request.user.role == 'ADMIN':
            return True

        # USER permissions
        user_permissions = guest_permissions + ['add_note', 'edit_own_link', 'view_own_stats']
        return permission_code in user_permissions

# Specific helper permissions
class CanShortenLink(permissions.BasePermission):
    def has_permission(self, request, view):
        return True  # All roles can shorten links

class CanAddNote(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['USER', 'ADMIN']

class CanEditLink(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['USER', 'ADMIN']

class CanViewStats(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['USER', 'ADMIN']

class CanManageAllLinks(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

class CanManageUsers(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'
