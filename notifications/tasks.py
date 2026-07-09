# tasks.py
from celery import shared_task
from asgiref.sync import async_to_sync
from .models import Notification
from .serializers import NotificationSerializer

try:
    from channels.layers import get_channel_layer
except ImportError:
    get_channel_layer = None

@shared_task(bind=True, max_retries=3)
def broadcast_notification_task(self, data, send_websocket=True):
    try:
        # Create notification (atomic)
        notification = Notification.objects.create(**data)
        if send_websocket and get_channel_layer:
            channel_layer = get_channel_layer()
            if channel_layer:
                group_name = f'notifications_{notification.recipient_id}'
                payload = NotificationSerializer(notification).data
                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        'type': 'notification.message',
                        'payload': payload,
                    }
                )
        return notification.id
    except Exception as exc:
        self.retry(exc=exc, countdown=60)