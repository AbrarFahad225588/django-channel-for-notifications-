# managers.py
from django.db import models
from django.utils import timezone

class NotificationQuerySet(models.QuerySet):
    def unread(self):
        return self.filter(is_read=False)
    
    def read(self):
        return self.filter(is_read=True)
    
    def for_recipient(self, user):
        return self.filter(recipient=user)
    
    def not_deleted(self):
        return self.filter(is_deleted=False)
    
    def mark_all_as_read(self, user):
        return self.for_recipient(user).unread().update(
            is_read=True,
            read_at=timezone.now()
        )

class NotificationManager(models.Manager.from_queryset(NotificationQuerySet)):
    def get_queryset(self):
        # If soft delete is enabled, exclude deleted by default
        return super().get_queryset().not_deleted()