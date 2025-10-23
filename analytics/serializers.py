from rest_framework import serializers
from .models import ClickStats


class ClickStatsSerializer(serializers.ModelSerializer):
    link_short_code = serializers.CharField(source='link.short_code', read_only=True)

    class Meta:
        model = ClickStats
        fields = ['id', 'link', 'link_short_code', 'clicked_at']
        read_only_fields = ['id', 'clicked_at']
