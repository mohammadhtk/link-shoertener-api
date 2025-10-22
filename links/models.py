from django.db import models
from django.conf import settings


# Create your models here.
class Link(models.Model):
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    custom_alias = models.CharField(max_length=50, unique=True, null=True, blank=True, db_index=True)
    original_url = models.URLField(max_length=2048)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='links')
    note = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    @property
    def short_url(self):
        return self.custom_alias if self.custom_alias else self.short_code

    @property
    def total_clicks(self):
        return self.clicks.count()

    class Meta:
        db_table = 'links'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['short_code']),
            models.Index(fields=['custom_alias']),
            models.Index(fields=['user', '-created_at']),
        ]

