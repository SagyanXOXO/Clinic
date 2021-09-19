from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length = 200, null = False, blank = False)

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'  

    def __str__(self):
        return(str(self.title))

class Specialization(models.Model):
    specialization = models.CharField(max_length = 250)
       

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = False, blank = False)
    job_title = models.ManyToManyField(Job)
    specialization = models.ManyToManyField(Specialization)
    education = models.TextField(blank = True, null = True)
    bio = models.TextField(verbose_name = 'Biography', null = True, blank = True)
    email = models.CharField(max_length = 250, blank = True, null = True)
    working_hours = models.TextField(blank = True, null = True)
    photo = models.FileField(upload_to = 'Employees')
    appointment = models.BooleanField(default = False, verbose_name = 'Taking Appointments ?')

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return(str(self.user))    
    
