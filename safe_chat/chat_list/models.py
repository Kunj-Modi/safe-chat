from django.contrib.auth.models import User
from django.db import models


class ChatList(models.Model):
    messageTo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_list_to')
    messageFrom = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_list_from')
    message_time = models.DateTimeField(auto_now_add=True)
    user_message = models.CharField(max_length=2000)

    def __str__(self):
        return f"To: {self.messageTo} From: {self.messageFrom}"
