# services.py
from celery import current_app
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from asgiref.sync import async_to_sync
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import broadcast_notification_task
from django.shortcuts import get_object_or_404

try:
    from channels.layers import get_channel_layer
except ImportError:
    get_channel_layer = None

def send_notification(
    recipient,
    actor=None,
    notification_type='SYSTEM',
    title='',
    message='',
    target=None,
    metadata=None,
    icon='',
    image='',
    action_url='',
    send_websocket=True,
    celery_async=True,
    **kwargs
):
    """
    Universal notification sender.
    
    All arguments are self‑explanatory. `target` can be any Django model instance.
    If `celery_async=True`, the database creation and WebSocket broadcast happen in a Celery task.
    """
    # Build data
    data = {
        'recipient': recipient,
        'actor': actor,
        'notification_type': notification_type,
        'title': title,
        'message': message,
        'metadata': metadata or {},
        'icon': icon,
        'image': image,
        'action_url': action_url,
        'target_content_type': None,
        'target_object_id': None,
    }
    
    if target:
        data['target_content_type'] = ContentType.objects.get_for_model(target)
        data['target_object_id'] = target.pk
    
    if celery_async:
        # Fire async task
        broadcast_notification_task.delay(data, send_websocket=send_websocket)
        return None
    else:
        # Synchronous creation and broadcast (for testing or immediate response)
        return _create_and_broadcast(data, send_websocket=send_websocket)

@transaction.atomic
def _create_and_broadcast(data, send_websocket=True):
    notification = Notification.objects.create(**data)
    if send_websocket:
        _broadcast_to_user(notification)
    return notification

def _broadcast_to_user(notification):
    if not get_channel_layer:
        return

    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    group_name = f'notifications_{notification.recipient_id}'
    payload = NotificationSerializer(notification).data
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'notification.message',
            'payload': payload,
        }
    )

def send_bulk_notification(
    recipients,  # list of user instances or IDs
    actor=None,
    notification_type='SYSTEM',
    title='',
    message='',
    target=None,
    metadata=None,
    **kwargs
):
    """
    Efficiently send one notification to many users.
    """
    # Avoid N+1 – build list of dicts
    notifications = []
    target_ct = None
    target_id = None
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        target_id = target.pk
    
    for recipient in recipients:
        notifications.append(
            Notification(
                recipient=recipient,
                actor=actor,
                notification_type=notification_type,
                title=title,
                message=message,
                metadata=metadata or {},
                target_content_type=target_ct,
                target_object_id=target_id,
                icon=kwargs.get('icon', ''),
                image=kwargs.get('image', ''),
                action_url=kwargs.get('action_url', ''),
            )
        )
    # Bulk create
    created = Notification.objects.bulk_create(notifications)
    # Broadcast each (could be batched to reduce channel calls)
    for notif in created:
        _broadcast_to_user(notif)
    return created

def mark_notification_as_read(notification_id, user):
    notification = get_object_or_404(Notification, id=notification_id, recipient=user)
    notification.mark_as_read()
    return notification

def mark_all_as_read(user):
    return Notification.objects.for_recipient(user).mark_all_as_read(user)

def get_unread_count(user):
    return Notification.objects.for_recipient(user).unread().count()


    