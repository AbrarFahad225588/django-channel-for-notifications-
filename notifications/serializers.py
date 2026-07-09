# serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'notification_type', 'title',
            'message', 'created_at', 'read_at', 'is_read',
            'target_content_type', 'target_object_id', 'metadata',
            'icon', 'image', 'action_url'
        ]
        read_only_fields = ['recipient', 'created_at', 'read_at']

class UnreadCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()