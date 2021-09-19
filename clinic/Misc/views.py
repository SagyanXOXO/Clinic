from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .models import Gallery, Pictures, Blog
from django.contrib import messages
from django.core.files import File
import json

com = {
    "comments" : [
        {
        "parent_id" : 0,
        "id" : 1,
        "name" : "John Cena",
        "comment" : "Cant see me",
        "time" : "3 hrs",
        "likes" : 0,
        "reply_count" : 2,
        "replies" : [
                    {
                    "parent_id" : 1,
                    "id" : 4,
                    "name" : "John Cena 2",
                    "comment" : "Cant see me 2",
                    "time" : "March 21st, 2021",
                    "likes" : 12,
                    "reply_count" : 1,
                    "replies" : [
                                {
                                    "parent_id" : 4,
                                    "id" : 9,
                                    "name" : "John Cena 2 4",
                                    "comment" : "Cant see me 2 4",
                                    "time" : "March 21st, 2021",
                                    "likes" : 21,
                                    "reply_count" : 0,
                                }
                                ]
                    },
                    {
                    "parent_id" : 1,
                    "id" : 98,
                    "name" : "Brock lesnae",
                    "comment" : "fuck u",
                    "time" : "March 21st, 2021",
                    "likes" : 98,
                    "reply_count" : 0,
                    }
                    ]
        },
        {
            "parent_id" : 0,
            "id" : 91,
            "name" : "Thread Ripper",
            "comment" : "New Thread",
            "time" : "March 21st, 2021",
            "likes" : 98,
            "reply_count" : 0,
        }
    ]
}


# These are the models for the admin
@method_decorator(user_passes_test(lambda u: u.is_superuser), name = 'dispatch')
class GalleryAdminView(View):
    def get(self, request):
        return render(request, 'cadmin/galleryadmin.html')

@method_decorator(user_passes_test(lambda u: u.is_superuser), name = 'dispatch')
class GalleryAdminAddView(View):
    def get(self, request):
        return render(request, 'cadmin/galleryadminadd.html') 

    def post(self, request):
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        images = request.FILES.getlist('my_pictures[]')
        submit = data.get('action')


        try:        
            gallery = Gallery(
                title = title,
                description = description
            )

            for i in images:
                picture = Pictures(
                    gallery = gallery,
                    pictures = i
                )
            gallery.save()
            if images:
                picture.save()

        except:
            messages.error(request, 'Sorry we ran into some problem.')

        else:
            messages.success(request, 'Record Successfully saved !!')

        if submit == 'save-btn':
            return HttpResponseRedirect('/admin/Misc/gallery') 
        elif submit == 'save-continue-btn':
            return HttpResponseRedirect(('/cadmin/Misc/gallery/change/' + str(gallery.id))) 
        else:
            return HttpResponseRedirect('/cadmin/Misc/gallery/add')    

        
        return render(request, 'cadmin/galleryadminadd.html')

@method_decorator(user_passes_test(lambda u: u.is_superuser), name = 'dispatch')
class GalleryAdminChangeView(View):
    def get(self,request,id):
        gallery = Gallery.objects.filter(id = id)
        pictures = Pictures.objects.filter(gallery = Gallery.objects.get(id = id))
        context = {'gallery' : gallery, 'pictures' : pictures}
        return render(request, 'cadmin/galleryadminchange.html', context)

    def post(self, request,id):
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        images = request.FILES.getlist('my_pictures[]')
        submit = data.get('action')
        preloaded = data.get('preloaded')

        if submit == 'delete-btn':
            gallery = Gallery.objects.get(id=id)
            gallery.delete()

        else:    
            if preloaded:
                preloaded = json.loads(preloaded)['images']

            try:
                gallery = Gallery.objects.get(id=id)
                if gallery:       
                    gallery.title = title
                    gallery.description = description

                    picture = Pictures.objects.filter(gallery = gallery)
                    for p in picture:
                        if '/media/' + str(p.pictures) not in preloaded:
                            picture = Pictures.objects.get(gallery = gallery, pictures = p.pictures).delete()

                    for i in images:
                        picture = Pictures(
                            gallery = gallery,
                            pictures = i
                        )  
                        picture.save()      

            except:
                messages.error(request, 'Sorry we ran into some problem.')

            else:    
                gallery.save()

                messages.success(request, 'Record Successfully updated !!')

        if submit == 'save-btn':
            return HttpResponseRedirect('/admin/Misc/gallery') 
        elif submit == 'save-continue-btn':
            return HttpResponseRedirect('/cadmin/Misc/gallery/change/' + str(gallery.id)) 
        elif submit == 'delete-btn':
            return HttpResponseRedirect('/admin/Misc/gallery') 
        else:
            return HttpResponseRedirect('/cadmin/Misc/gallery/add')    

        
        return render(request, 'cadmin/galleryadminadd.html')    


# Views for rendering frontend
class BlogView(View):
    pass

class DetailBlogView(View):
    def get(self,request,id):
        if request.is_ajax():
            return JsonResponse({'comments' : json.dumps(com)})
        blog = Blog.objects.get(id = id)
        context = {'blog' : blog}
        return render(request, 'detail_blog.html',context)            





