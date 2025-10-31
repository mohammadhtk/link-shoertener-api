from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with simple role-based access (no Role/Permission tables)"""

    GUEST = 'GUEST'
    USER = 'USER'
    ADMIN = 'ADMIN'

    ROLE_CHOICES = [
        (GUEST, 'Guest'),
        (USER, 'User'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
        help_text='Defines access level for the user'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_guest(self):
        return self.role == self.GUEST

    def has_permission(self, permission_code):
        # Map simplified role-based permissions.
        # Guests have limited default permissions.
        guest_permissions = ['shorten_link_random', 'shorten_link_custom']
        if self.is_guest:
            return permission_code in guest_permissions
        elif self.is_admin:
            return True  # Admin has all permissions
        else:
            # Regular user permissions
            user_permissions = guest_permissions + [
                'add_note', 'edit_own_link', 'view_own_stats'
            ]
            return permission_code in user_permissions

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
