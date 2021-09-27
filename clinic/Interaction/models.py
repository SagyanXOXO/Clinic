from django.db import models
from Misc.models import Blog
from datetime import datetime
from django.contrib.auth.models import User


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, blank = True, null = True)
    reply = models.ForeignKey('self', on_delete = models.CASCADE, blank = True, null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default = datetime.now)

    def __str__(self):
        return str(self.id)

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, blank = True, null = True)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE, blank = True, null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.id)



