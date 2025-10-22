import pytest
from links.models import Link
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestLinkModel:
    def test_create_link(self):
        link = Link.objects.create(
            short_code='abc123',
            original_url='https://example.com'
        )
        assert link.short_code == 'abc123'
        assert link.original_url == 'https://example.com'
        assert link.is_active

    def test_link_with_custom_alias(self):
        link = Link.objects.create(
            short_code='abc123',
            custom_alias='mylink',
            original_url='https://example.com'
        )
        assert link.short_url == 'mylink'

    def test_link_without_custom_alias(self):
        link = Link.objects.create(
            short_code='abc123',
            original_url='https://example.com'
        )
        assert link.short_url == 'abc123'
