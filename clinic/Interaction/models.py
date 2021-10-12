from django.db import models
from Misc.models import Blog
from datetime import datetime
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, blank = True, null = True)
    reply = models.ForeignKey('self', on_delete = models.CASCADE, blank = True, null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return str(self.content)

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, blank = True, null = True)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE, blank = True, null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.id)


class Notification(models.Model):
    title = models.CharField(max_length = 250)
    sender = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    receiver = models.ManyToManyField(User, related_name = 'receiver')
    timestamp = models.DateTimeField(auto_now_add = True)
    redirect_url = models.TextField(blank = True, null = True)
    has_viewed = models.BooleanField(default = False)        

    def __str__(self):
        return str(self.title)
  



