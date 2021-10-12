from django.shortcuts import render
from django.views import View
from .models import Notification
from django.http import JsonResponse, HttpResponse
import json
from django.core.serializers import serialize

def notification_serializer(noti):
    for n in noti:
        print(n)
    return noti

class NotificationView(View):
    def get(self, request):
        if request.is_ajax() and request.user.is_staff: 
            action = request.GET.get('action')
            if action.lower() == 'get_notification':
                notification = Notification.objects.filter(receiver__in = [request.user])    
                notification = serialize('json', notification)
                notification = json.loads(notification)
                


            return JsonResponse({'notification' : notification})


    def post(self, request):
        pass          
