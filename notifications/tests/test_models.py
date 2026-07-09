from django.test import TestCase
from ..models import Notification
from django.contrib.auth import get_user_model


class NotificationModelTests(TestCase):
    def test_create_notification(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='pass')
        n = Notification.objects.create(recipient=user, verb='hello')
        self.assertEqual(str(n).startswith('Notification('), True)
