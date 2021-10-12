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
        "has_liked" : 0,
        "reply_count" : 2,
        },
                    {
                    "parent_id" : 1,
                    "id" : 4,
                    "name" : "John Cena 2",
                    "comment" : "Cant see me 2",
                    "time" : "M",
                    "likes" : 12,
                    "has_liked" : 0,
                    "reply_count" : 1,
                    },
                                {
                                    "parent_id" : 4,
                                    "id" : 9,
                                    "name" : "John Cena 2 4",
                                    "comment" : "Cant see me 2 4",
                                    "time" : "M",
                                    "likes" : 21,
                                    "has_liked" : 0,
                                    "reply_count" : 0,
                                },
                    {
                    "parent_id" : 1,
                    "id" : 98,
                    "name" : "Brock lesnae",
                    "comment" : "fuck u",
                    "time" : "M",
                    "likes" : 98,
                    "has_liked" : 0,
                    "reply_count" : 0,
                    },
        {
            "parent_id" : 0,
            "id" : 91,
            "name" : "Thread Ripper",
            "comment" : "New Thread",
            "time" : "March 21st, 2021",
            "likes" : 98,
            "has_liked" : 0,
            "reply_count" : 0,
        }
    ]
}

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def comment_constructor(blog,user):
    comments = {"comments" : []}

    # Construct nested comment json thread
    comment = Comment.objects.filter(blog = blog)
    for c in comment:
        comment_dict = {}

        comment_dict.update({'id' : c.id, 'name' : c.user.username, 'comment' : c.content, 'time' : str(c.timestamp)})
        if c.reply:
            comment_dict.update({'parent_id' : c.reply.id})
        else:
            comment_dict.update({'parent_id' : 0})

        # Get total likes    
        likes_count = Like.objects.filter(comment = c)
        comment_dict.update({"likes" : len(likes_count)}) 

        # Check if the current user has liked this particular comment
        if user.is_authenticated:
            has_liked = Like.objects.filter(comment = c, user = user)
        else:
            has_liked = 0    
        if has_liked:
            comment_dict.update({'has_liked' : 1})
        else:
            comment_dict.update({'has_liked' : 0})    

        # Get total replies
        replies = Comment.objects.filter(reply = c)


        comments['comments'].append(comment_dict)

    #print(comments)    
    return comments   



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
            comments = comment_constructor(Blog.objects.get(id = id), current_user)
            return JsonResponse({'comments' : json.dumps(comments)})

        for key, value in request.session.items():
            print('{} => {}'.format(key, value))    

        # Increment the view
        if 'has_viewed' not in request.session:
            blog = Blog.objects.get(id = id)
            blog.views = blog.views + 1    
            blog.save()

            request.session['has_viewed'] = True

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
        else:
            has_liked = 0    

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
                _content = request.POST.get('comment')
                #print(_content)

                if action.lower() == 'like':
                    if _parent.lower() == 'blog':
                        try:
                            blog = Blog.objects.get(id = _id)

                        except ObjectDoesNotExist:
                            print('Blog does not exist')

                        else:        
                            like = Like.objects.filter(blog = blog)
                            if not like:
                                try:
                                    Like.objects.create(blog = blog, user = current_user).save()
                                except:    
                                    return JsonResponse({'message' : 'Something went wrong.'})  
                                else:
                                    return JsonResponse({'message' : 'You have liked this post.'})      
                            else:
                                try:
                                    like.delete()
                                except:
                                    return JsonResponse({'message' : 'Something went wrong.'}) 
                                else:
                                    return JsonResponse({'message' : 'You have unliked this post.'})          
                    elif _parent.lower() == 'comment':
                        try:
                            comment = Comment.objects.get(id = _id)
                        except ObjectDoesNotExist:
                            print('Comment does not exist')    
                        else:
                            like = Like.objects.filter(comment = comment)
                            if not like:
                                try:
                                    Like.objects.create(comment = comment, user = current_user).save()
                                except:
                                    return JsonResponse({'message' : 'Something went wrong.'})
                                else:
                                    return JsonResponse({'message' : 'You have liked this comment'}) 
                            else:
                                try:
                                    like.delete()
                                except:
                                    return JsonResponse({'message' : 'Something went wrong'})
                                else:
                                    return JsonResponse({'message' : 'You have unliekd this comment'})                           
                           

                elif action.lower() == 'comment':
                    if _parent.lower() == 'blog':
                        try:
                            blog = Blog.objects.get(id = _id)

                        except ObjectDoesNotExist:  
                            pass

                        else:      
                            try:
                                Comment.objects.create(blog = blog, user = current_user, content = _content).save()

                            except:
                                return JsonResponse({'message' : 'Something went wrong.'})

                            else:        
                                return JsonResponse({'message' : 'Your comment has been posted.'})

                    elif _parent.lower() == 'comment':
                        try:
                            comment = Comment.objects.get(id = _id)

                        except ObjectDoesNotExist:
                            pass

                        else:
                            try:
                                Comment.objects.create(blog = comment.blog, reply = comment, user = current_user, content = _content).save()

                            except:
                                return JsonResponse({'message' : 'Something went wrong'})  

                            else:
                                return JsonResponse({'message' : 'Your comment has been posted'})   

            return JsonResponse({'success' : 'true'})            



        else:
            print('Not logged in ...')
            return JsonResponse({'message' : 'User not logged in'})            





