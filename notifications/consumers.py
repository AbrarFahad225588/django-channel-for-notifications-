# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification
from .serializers import NotificationSerializer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')

        if not self.user or getattr(self.user, 'is_anonymous', True):
            await self.close()
            return

        self.group_name = f'notifications_{self.user.id}'
        try:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            print("Consumer group:", self.group_name)
        except Exception:
            await self.close()
            return

        await self.accept()
        await self.send(text_data=json.dumps({
            "message": "Connected!"
        }))

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            try:
                await self.channel_layer.group_discard(
                    self.group_name,
                    self.channel_name
                )
            except Exception:
                pass

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({
            "message": text_data
        }))

    async def notification_message(self, event):
        """Handler for messages sent to the group."""
        payload = event.get('payload', {})
        await self.send(text_data=json.dumps(payload))