from django.contrib.auth.models import AbstractUser
from django.db import models

# Permission model for RBAC
class Permission(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'permissions'
        ordering = ['name']

# Role model for RBAC
class Role(models.Model):
    GUEST = 'Guest'
    USER = 'User'
    ADMIN = 'Admin'

    ROLE_CHOICES = [
        (GUEST, 'Guest'),
        (USER, 'User'),
        (ADMIN, 'Admin'),
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, related_name='roles', blank=True)

    def __str__(self):
        return self.name


    def has_permission(self, permission_code):
        # Check if role has a specific permission
        return self.permissions.filter(code=permission_code).exists()

    class Meta:
        db_table = 'roles'
        ordering = ['name']


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role and self.role.name == Role.ADMIN

    @property
    def is_guest(self):
        return self.role is None or self.role.name == Role.GUEST

    def has_permission(self, permission_code):
        # Check if user has a specific permission through their role
        if not self.role:
            # Guest users have limited permissions
            return permission_code in ['shorten_link_random', 'shorten_link_custom']
        return self.role.has_permission(permission_code)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
