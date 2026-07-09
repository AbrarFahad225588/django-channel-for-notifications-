# selectors.py
from django.db.models import Q
from .models import Notification

def get_notifications(user, filters=None, page=1, page_size=20):
    qs = Notification.objects.for_recipient(user).select_related('actor')
    # optional prefetch if target is commonly used
    # qs = qs.prefetch_related('target')
    if filters:
        if 'is_read' in filters:
            qs = qs.filter(is_read=filters['is_read'])
        if 'notification_type' in filters:
            qs = qs.filter(notification_type=filters['notification_type'])
    # Order: unread first, then newest
    qs = qs.order_by('-is_read', '-created_at')
    # Pagination (manual or DRF's paginator)
    start = (page - 1) * page_size
    end = start + page_size
    return list(qs[start:end]), qs.count()