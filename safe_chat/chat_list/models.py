from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_chats')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_chats')
    last_message = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f"Chat ID: {self.chat_id}, Users: {self.user1.username} - {self.user2.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group_name = [self.user1.username, self.user2.username]
        channel_layer = get_channel_layer()
        for group in group_name:
            if group in channel_layer.groups:
                sender = self.user1.username if self.user1.username != group else self.user2.username
                async_to_sync(channel_layer.group_send)(
                    group,
                    {
                        'type': 'list_update',
                        'sender': sender,
                    }
                )


class Message(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    message_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat ID: {self.chat_id.chat_id}, From: {self.from_user.username}, Time: {self.message_time}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        group_name = f"group{self.chat_id.chat_id}"
        print(group_name)
        channel_layer = get_channel_layer()

        if group_name in channel_layer.groups:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'message',
                    'from_user': self.from_user.username,
                    'message': self.message,
                }
            )
