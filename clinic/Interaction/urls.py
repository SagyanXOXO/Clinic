from django.urls import path,include
from .views import NotificationView

urlpatterns = [
    path('cadmin/notification/', NotificationView.as_view(), name = 'admin_notification')
]