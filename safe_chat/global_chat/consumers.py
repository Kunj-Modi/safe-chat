import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import GlobalChat


class GlobalConsumer(WebsocketConsumer):
    def send_message(self, event):
        user = event['user']
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'message',
            'user': user,
            'message': message,
        }))

    def connect(self, *args, **kwargs):
        group_name = 'global_chat'
        async_to_sync(self.channel_layer.group_add)(
            group_name,
            self.channel_name
        )

        user = self.scope.get('user')
        if user and user.is_authenticated:
            self.accept()
        else:
            self.close()

    def receive(self, text_data, *args, **kwargs):
        user = self.scope.get('user')
        text_data = text_data[12:-2]
        if user and text_data.strip():
            GlobalChat.objects.create(user=user, user_message=text_data)

            async_to_sync(self.channel_layer.group_send)(
                'global_chat',
                {
                    'type': 'send_message',
                    'user': user.username,
                    'message': text_data,
                }
            )

    def disconnect(self, *args, **kwargs):
        self.close()
