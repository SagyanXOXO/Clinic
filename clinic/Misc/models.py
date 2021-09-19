from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from Personnel.models import Employee

blog_choices = (
    ('DRAFT', 'draft'),
    ('PUBLISH', 'publish') 
)

class Gallery(models.Model):
    title = models.CharField(max_length = 250, blank = False, null = False)
    description = models.TextField(blank = True, null = True)

    def __str__(self):
        return(str(self.title))
    
    
class Pictures(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete = models.CASCADE)  
    pictures = models.FileField(upload_to = 'gallery')
    
class Blog(models.Model):
    title = models.CharField(max_length = 250)
    author = models.ForeignKey(Employee, on_delete = models.CASCADE, null = True, blank = True)
    publish_date = models.DateTimeField(default = datetime.now, blank = True)
    tags = TaggableManager(blank = True)
    thumbnail = models.FileField(upload_to = 'blog', blank = True, null = True)
    views = models.PositiveIntegerField(default = 0)
    status = models.CharField(max_length = 7, choices = blog_choices, default = 'DRAFT')

    # The blog Tinymce section
    content = RichTextUploadingField()

    def __str__(self):
        return str(self.title)

    

        
