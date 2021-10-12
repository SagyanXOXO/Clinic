from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import Notification, Like
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from . import notifications
    

# This channel uses redis as a backing store
# Channel layer and redis configured in settings
# Redis server running from docker image
# channel_name gets created automatically if properly initialized
# AsyncWebSocketConsumer used and also group created
class AdminNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = self.user.username + '_' + str(self.user.id)
        print(self.group_name)

        if (self.user.is_superuser):
            await self.accept()

            # Join admin_group group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

   
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass       

    async def admin_notify(self,event):
        await self.send(event['data'])    


  
  



