from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Like, Notification
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


@receiver(post_save, sender = Notification)
def after_receiver(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    message = str(instance.title).capitalize()
    _sender = str(instance.sender.username)
    timestamp = str(instance.timestamp)
    redirect_url = str(instance.redirect_url)
    for i in instance.receiver.all():
        group_name = str(i.username) + '_' + str(i.id)
        async_to_sync(channel_layer.group_send)(
            group_name,
                {
                    'type' : 'admin_notify',
                    'data' : json.dumps({
                        'message' : message,
                        'sender' : _sender,
                        'timestamp' : timestamp,
                        'redirect_url' : redirect_url
                    })
                }
            )      
         

@receiver(post_save, sender = Like)
def callback_like(sender, instance, created, **kwargs):
    if created:
        _sender = instance.user
    
        if instance.blog:
            title = str(_sender).capitalize() + ' ' + 'liked your blog' + ' ' + str(instance.blog.title)
        else:
            title = str(_sender).capitalize() + ' ' + 'liked your comment' + ' ' + str(instance.comment.content)
            
        try:
            notification = Notification(
                    title = title,
                    sender  = _sender
                )

            notification.save()      

    
        except Exception as e:
            print(e) 

        else:
            staff = User.objects.filter(is_staff = True)
            for u in staff:    
                user = User.objects.get(id = u.id)
                notification.receiver.add(user)

            notification.save()    
     
  

    



         


 


