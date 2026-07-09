from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Notification
from ..services import mark_all_as_read


class NotificationServiceTests(TestCase):
    def test_mark_all_as_read(self):
        User = get_user_model()
        user = User.objects.create_user(username='svcuser', password='pass')
        Notification.objects.create(recipient=user, verb='one')
        Notification.objects.create(recipient=user, verb='two', unread=False)
        updated = mark_all_as_read(user)
        self.assertEqual(updated, 1)
