from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import ClickStats


class AnalyticsService:

    # Track a click on a link (privacy-safe - no personal data)
    @staticmethod
    def track_click(link):

        return ClickStats.objects.create(link=link)

    # Get stats for a link (privacy-safe)
    @staticmethod
    def get_link_stats(link):
        clicks = link.clicks.all()

        # Total clicks
        total_clicks = clicks.count()

        # Recent click timestamps
        recent_clicks = clicks.order_by('-clicked_at')[:20].values('clicked_at')

        # Daily clicks (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_clicks = clicks.filter(clicked_at__gte=thirty_days_ago).extra(
            select={'day': 'DATE(clicked_at)'}
        ).values('day').annotate(count=Count('id')).order_by('day')

        # Weekly clicks (last 12 weeks)
        twelve_weeks_ago = timezone.now() - timedelta(weeks=12)
        weekly_clicks = clicks.filter(clicked_at__gte=twelve_weeks_ago).extra(
            select={'week': "DATE_TRUNC('week', clicked_at)"}
        ).values('week').annotate(count=Count('id')).order_by('week')

        return {
            'total_clicks': total_clicks,
            'recent_clicks': list(recent_clicks),
            'daily_clicks': list(daily_clicks),
            'weekly_clicks': list(weekly_clicks),
        }

    # Get global analytics stats
    @staticmethod
    def get_global_stats():
        from links.models import Link
        from users.models import User

        total_links = Link.objects.count()
        active_links = Link.objects.filter(is_active=True).count()
        total_clicks = ClickStats.objects.count()
        total_users = User.objects.count()

        # Top performing links
        top_links = Link.objects.annotate(
            click_count=Count('clicks')
        ).order_by('-click_count')[:10]

        return {
            'total_links': total_links,
            'active_links': active_links,
            'total_clicks': total_clicks,
            'total_users': total_users,
            'top_links': [
                {
                    'short_code': link.short_code,
                    'original_url': link.original_url,
                    'clicks': link.click_count
                }
                for link in top_links
            ]
        }
