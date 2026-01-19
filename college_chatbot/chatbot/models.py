from django.db import models
from django.contrib.auth.models import User


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_message




