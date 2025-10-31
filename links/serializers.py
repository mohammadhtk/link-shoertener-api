from rest_framework import serializers
from .models import Link

# Serializer for viewing Link details
class LinkSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(read_only=True)
    total_clicks = serializers.IntegerField(read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    click_timestamps = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = [
            'id', 'short_code', 'custom_alias', 'short_url', 'original_url',
            'user', 'user_username', 'note', 'is_active', 'total_clicks',
            'click_timestamps', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'short_code', 'user', 'created_at', 'updated_at', 'short_url', 'total_clicks', 'click_timestamps']

    def get_click_timestamps(self, obj):
        return [click.clicked_at for click in obj.clicks.order_by('-clicked_at')[:10]]


# Serializer for creating a new Link
class LinkCreateSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(read_only=True)
    total_clicks = serializers.IntegerField(read_only=True)
    click_timestamps = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ['original_url', 'custom_alias', 'note', 'short_url', 'total_clicks', 'click_timestamps']

    def validate_original_url(self, value):
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("URL must start with http:// or https://")
        return value

    def validate_custom_alias(self, value):
        if value and Link.objects.filter(custom_alias=value).exists():
            raise serializers.ValidationError("This custom alias is already taken")
        return value

    def get_click_timestamps(self, obj):
        return [click.clicked_at for click in obj.clicks.order_by('-clicked_at')[:10]]

    def create(self, validated_data):
        link = super().create(validated_data)
        # populate computed fields
        link.short_url = link.short_url
        link.total_clicks = link.total_clicks
        return link


# Serializer for updating an existing Link
class LinkUpdateSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(read_only=True)
    total_clicks = serializers.IntegerField(read_only=True)
    click_timestamps = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ['original_url', 'note', 'is_active', 'short_url', 'total_clicks', 'click_timestamps']

    def get_click_timestamps(self, obj):
        return [click.clicked_at for click in obj.clicks.order_by('-clicked_at')[:10]]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.short_url = instance.short_url
        instance.total_clicks = instance.total_clicks
        return instance
