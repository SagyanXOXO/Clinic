from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
import json
from .models import Job, Employee

# Views for admin starts here

@method_decorator(user_passes_test(lambda u: u.is_superuser), name = 'dispatch')
class EmployeeAdminView(View):
    def get(self, request):
        if request.is_ajax():
            user = User.objects.all().values('username')
            job = Job.objects.all().values()
            context = {'User' : list(user), 'Job' : list(job)}
            return JsonResponse(context)
        else:
            return HttpResponse('Hello')   

    def post(self, request):
        values = request.POST
        user = values.get('user')
        _user = User.objects.get(username = user)
        job = values.getlist('job')
        _job = Job.objects.get(title__in = job)
        bio = values.get('bio')
        photo = request.FILES['my-photo']
        
        emp = Employee(user = _user, job_title = _job, bio = bio, photo = photo)
        emp.save()
        return HttpResponseRedirect('/admin/Personnel/employee/add/')