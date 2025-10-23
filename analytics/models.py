from django.db import models
from links.models import Link

# Create your models here.
class ClickStats(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Click on {self.link.short_code} at {self.clicked_at}"

    class Meta:
        db_table = 'click_stats'
        ordering = ['-clicked_at']
        indexes = [
            models.Index(fields=['link', '-clicked_at']),
        ]
        verbose_name_plural = 'Click Stats'
