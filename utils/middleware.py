from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from links.models import Link
from analytics.services import AnalyticsService


class ClickTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to track clicks on shortened links.
    Intercepts requests to short codes and records analytics before redirecting.
    """

    def process_request(self, request):
        # Skip if not a potential short link request
        path = request.path.strip('/')

        # Skip API endpoints and admin
        if path.startswith('api/') or path.startswith('admin/'):
            return None

        # Skip if path has multiple segments (not a short code)
        if '/' in path:
            return None

        # Skip if empty path
        if not path:
            return None

        # Try to find link by short code
        try:
            link = Link.objects.get(short_code=path)
        except Link.DoesNotExist:
            # Try custom alias
            try:
                link = Link.objects.get(custom_alias=path)
            except Link.DoesNotExist:
                return None

        # Check if link is active
        if not link.is_active:
            from django.http import HttpResponse
            return HttpResponse('Link is inactive', status=410)

        AnalyticsService.track_click(link=link)

        return redirect(link.original_url)
