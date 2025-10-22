import pytest
from links.services import LinkService


@pytest.mark.django_db
class TestLinkService:
    def test_generate_short_code(self):
        code = LinkService.generate_short_code()
        assert len(code) == 6
        assert code.isalnum()

    def test_create_link(self):
        link = LinkService.create_link(
            original_url='https://example.com',
            note='Test link'
        )
        assert link.original_url == 'https://example.com'
        assert link.note == 'Test link'
        assert link.short_code

    def test_create_link_with_custom_alias(self):
        link = LinkService.create_link(
            original_url='https://example.com',
            custom_alias='mylink'
        )
        assert link.custom_alias == 'mylink'

    def test_update_link(self):
        link = LinkService.create_link(original_url='https://example.com')
        updated_link = LinkService.update_link(
            link=link,
            original_url='https://newurl.com',
            is_active=False
        )
        assert updated_link.original_url == 'https://newurl.com'
        assert not updated_link.is_active

    def test_get_link_by_code(self):
        link = LinkService.create_link(
            original_url='https://example.com',
            custom_alias='mylink'
        )

        # Test by short_code
        found_link = LinkService.get_link_by_code(link.short_code)
        assert found_link.id == link.id

        # Test by custom_alias
        found_link = LinkService.get_link_by_code('mylink')
        assert found_link.id == link.id

        # Test not found
        not_found = LinkService.get_link_by_code('nonexistent')
        assert not_found is None
