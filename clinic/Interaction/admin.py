from django.contrib import admin
from .models import Like, Comment,Notification

class LikeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Like,LikeAdmin)    

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, CommentAdmin) 

class NotificationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Notification, NotificationAdmin) 
