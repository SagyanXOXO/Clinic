from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .models import Gallery, Pictures, Blog
from Interaction.models import Comment, Like
from django.contrib import messages
from django.core.files import File
import json
from django.core.exceptions import ObjectDoesNotExist

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
                    "time" : "M",
                    "likes" : 12,
                    "reply_count" : 1,
                    "replies" : [
                                {
                                    "parent_id" : 4,
                                    "id" : 9,
                                    "name" : "John Cena 2 4",
                                    "comment" : "Cant see me 2 4",
                                    "time" : "M",
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
                    "time" : "M",
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
        current_user = request.user
        if request.is_ajax():
            return JsonResponse({'comments' : json.dumps(com)})

        # Get blog total likes
        total_likes = Like.objects.filter(blog = Blog.objects.get(id = id))
        total_likes = len(total_likes)

        # Get blog total comments    
        total_comments = Comment.objects.filter(blog = Blog.objects.get(id = id))
        total_comments = len(total_comments)

        # Check if the current user has liked the blog or not
        if current_user.is_authenticated:
            has_liked = Like.objects.filter(blog = Blog.objects.get(id = id), user = current_user)
            has_liked = len(has_liked)
            print(has_liked)

        # Construct nested comment json thread
        blog = Blog.objects.get(id = id)
        context = {'blog' : blog, 'total_likes' : total_likes, 'total_comments' : total_comments, 'has_liked' : has_liked}
        return render(request, 'detail_blog.html',context)  

    def post(self,request,id):
        current_user = request.user
        # Need to login to use any POST method
        if current_user.is_authenticated:
            # Determine course of action using the action and the action-id   
            if request.is_ajax():
                action = request.POST.get('action')
                _id = request.POST.get('id')   
                _parent = request.POST.get('parent')  
                print(_parent)

                if action.lower() == 'like':
                    if _parent.lower() == 'blog':
                        blog = Blog.objects.get(id = _id)
                        try:
                            like = Like.objects.get(blog = blog)
                        except ObjectDoesNotExist:
                            Like.objects.create(blog = blog, user = current_user).save()   
                        else:
                            like.delete() 
                    if _parent.lower() == 'comment':
                        pass                
                elif action.lower() == 'comment':
                    if _parent.lower() == 'blog':
                        blog = Blog.objects.get(id = _id)
                        Comment.objects.create(blog = blog, user = current_user)
                    if _parent.lower() == 'comment':
                        pass 
            return JsonResponse({'data' : 'sd'})            



        else:
            print('Not logged in ...')            





