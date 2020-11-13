from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
print(models.Model)
class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"message from {self.author.username} at {self.timestamp.date}"
    
    def get_last_10_message():
        return Message.objects.order_by("-timestamp")[:10][::-1]
