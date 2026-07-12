import json
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Notification
from ..services import mark_all_as_read, prepare_notification_data, send_notification


class NotificationServiceTests(TestCase):
    def test_mark_all_as_read(self):
        User = get_user_model()
        user = User.objects.create_user(username='svcuser', password='pass')
        Notification.objects.create(
            recipient=user,
            notification_type='SYSTEM',
            title='one',
            message='first'
        )
        Notification.objects.create(
            recipient=user,
            notification_type='SYSTEM',
            title='two',
            message='second',
            is_read=True
        )
        updated = mark_all_as_read(user)
        self.assertEqual(updated, 1)

    def test_prepare_notification_data_uses_serializable_ids(self):
        User = get_user_model()
        recipient = User.objects.create_user(username='recipient', password='pass')
        actor = User.objects.create_user(username='actor', password='pass')

        payload = prepare_notification_data(
            recipient=recipient,
            actor=actor,
            title='Hello',
            message='World',
        )

        self.assertEqual(payload['recipient_id'], recipient.id)
        self.assertEqual(payload['actor_id'], actor.id)
        self.assertEqual(payload['title'], 'Hello')
        self.assertEqual(payload['message'], 'World')
        self.assertIsInstance(json.dumps(payload), str)

    def test_send_notification_falls_back_to_synchronous_save_when_celery_fails(self):
        User = get_user_model()
        recipient = User.objects.create_user(username='fallback', password='pass')

        with patch('notifications.services.broadcast_notification_task.delay', side_effect=Exception('broker down')):
            notification = send_notification(
                recipient,
                actor=None,
                title='Fallback save',
                message='Stored without celery',
            )

        self.assertIsNotNone(notification)
        self.assertTrue(
            Notification.objects.filter(
                recipient=recipient,
                title='Fallback save',
                message='Stored without celery',
            ).exists()
        )
