# tasks.py
from celery import shared_task
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import Notification
from .serializers import NotificationSerializer

try:
    from channels.layers import get_channel_layer
except ImportError:
    get_channel_layer = None

@shared_task(bind=True, max_retries=3)
def broadcast_notification_task(self, data, send_websocket=True):
    try:
        recipient_id = data.pop('recipient_id', None)
        actor_id = data.pop('actor_id', None)
        recipient = get_user_model().objects.filter(id=recipient_id).first() if recipient_id else None
        actor = get_user_model().objects.filter(id=actor_id).first() if actor_id else None

        if not recipient:
            return None

        notification = Notification.objects.create(
            recipient=recipient,
            actor=actor,
            **data
        )
        if send_websocket and get_channel_layer:
            try:
                channel_layer = get_channel_layer()
            except Exception:
                channel_layer = None

            if channel_layer:
                try:
                    group_name = f'notifications_{notification.recipient_id}'
                    payload = NotificationSerializer(notification).data
                    async_to_sync(channel_layer.group_send)(
                        group_name,
                        {
                            'type': 'notification_message',
                            'payload': payload,
                        }
                    )
                except Exception:
                    pass
        return notification.id
    except Exception as exc:
        self.retry(exc=exc, countdown=60)