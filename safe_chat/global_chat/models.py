from django.db import models
from django.contrib.auth.models import User


class GlobalChat(models.Model):
    message_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_message = models.CharField(max_length=2000)

    def __str__(self):
        return self.user_message
