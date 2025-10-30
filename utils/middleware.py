from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from links.models import Link
from analytics.services import AnalyticsService


class ClickTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to track clicks on shortened links.
    DISABLED: API now returns JSON for mobile apps instead of server-side redirects.
    """
    pass