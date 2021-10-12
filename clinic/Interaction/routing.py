from django.urls import path, include, re_path
from .consumers import AdminNotificationConsumer

ws_urlpatterns = [
    path('ws/notifications/', AdminNotificationConsumer.as_asgi())
]