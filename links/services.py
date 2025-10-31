import string
import random
from .models import Link

class LinkService:
    @staticmethod
    def generate_short_code(length=6):
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choices(characters, k=length))
            if not Link.objects.filter(short_code=short_code).exists():
                return short_code

    @staticmethod
    def create_link(original_url, user=None, custom_alias=None, note=''):
        short_code = LinkService.generate_short_code()
        link = Link.objects.create(
            short_code=short_code,
            custom_alias=custom_alias,
            original_url=original_url,
            user=user,
            note=note
        )
        return link

    @staticmethod
    def update_link(link, original_url=None, note=None, is_active=None):
        if original_url is not None:
            link.original_url = original_url
        if note is not None:
            link.note = note
        if is_active is not None:
            link.is_active = is_active
        link.save()
        return link

    @staticmethod
    def get_link_by_code(code):
        try:
            return Link.objects.get(short_code=code, is_active=True)
        except Link.DoesNotExist:
            try:
                return Link.objects.get(custom_alias=code, is_active=True)
            except Link.DoesNotExist:
                return None
