from rest_framework import serializers
from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(read_only=True)
    total_clicks = serializers.IntegerField(read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Link
        fields = [
            'id', 'short_code', 'custom_alias', 'short_url', 'original_url',
            'user', 'user_username', 'note', 'is_active', 'total_clicks',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'short_code', 'user', 'created_at', 'updated_at']


class LinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['original_url', 'custom_alias', 'note']

    def validate_original_url(self, value):
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("URL must start with http:// or https://")
        return value

    def validate_custom_alias(self, value):
        if value and Link.objects.filter(custom_alias=value).exists():
            raise serializers.ValidationError("This custom alias is already taken")
        return value


class LinkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['original_url', 'note', 'is_active']
