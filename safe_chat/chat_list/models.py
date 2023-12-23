from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_chats')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_chats')
    last_message = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f"Chat ID: {self.chat_id}, Users: {self.user1.username} - {self.user2.username}"


class Message(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    message_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat ID: {self.chat_id.chat_id}, From: {self.from_user.username}, Time: {self.message_time}"
