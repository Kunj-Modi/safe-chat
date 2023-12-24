from datetime import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from chat_list.models import Chat, Message
from django.db.models import Q


class ChatConsumer(WebsocketConsumer):
    def message(self, event):
        self.send(text_data=json.dumps({
            'type': 'list_update',
            'from': event['from_user'],
            'message': event["message"],
        }))

    def connect(self, *args, **kwargs):
        other = self.scope['url_route']['kwargs']['other']
        user = self.scope.get('user')
        if user and user.is_authenticated:
            receiver = User.objects.get(username=user)
            sender = User.objects.get(username=other)
            chat_id = Chat.objects.get(
                Q(user1=receiver.id, user2=sender.id) | Q(user1=sender.id, user2=receiver.id)).chat_id
            group_name = f"group{chat_id}"
            print(group_name)
            async_to_sync(self.channel_layer.group_add)(
                group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def receive(self, text_data, *args, **kwargs):
        user = User.objects.get(username=self.scope.get('user'))
        other = self.scope['url_route']['kwargs']['other']
        sender = User.objects.get(username=other)
        chat_id = Chat.objects.get(Q(user1=user.id, user2=sender.id) | Q(user1=sender.id, user2=user.id))
        user_message = text_data[12:-2]
        chat_id.last_message = datetime.now()
        chat_id.save()
        if user_message != "":
            Message.objects.create(chat_id=chat_id, from_user=user, message=user_message)

    def disconnect(self, *args, **kwargs):
        self.close()
