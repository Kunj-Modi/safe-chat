import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Chat


class ChatListConsumer(WebsocketConsumer):
    def list_update(self, event):
        sender = event['sender']

        self.send(text_data=json.dumps({
            'type': 'list_update',
            'sender': sender,
        }))

    def connect(self, *args, **kwargs):
        user = self.scope.get('user')
        group_name = user.username
        if group_name:
            async_to_sync(self.channel_layer.group_add)(
                group_name,
                self.channel_name
            )

        if user and user.is_authenticated:
            self.accept()
        else:
            self.close()

    def receive(self, text_data, *args, **kwargs):
        pass

    def disconnect(self, *args, **kwargs):
        self.close()
