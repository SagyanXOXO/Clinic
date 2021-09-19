from django.urls import path
from .views import GalleryAdminView, GalleryAdminAddView, GalleryAdminChangeView,BlogView,DetailBlogView

urlpatterns = [
    #path('Misc/Gallery/', GalleryAdminView.as_view(), name = 'gallery_admin'),
    path('cadmin/Misc/gallery/add', GalleryAdminAddView.as_view(), name = 'gallery_admin_add'),
    path('cadmin/Misc/gallery/change/<id>', GalleryAdminChangeView.as_view(), name = 'gallery_admin_change'),
    path('blogs/',BlogView.as_view(), name = 'blog'),
    path('blog/<id>',DetailBlogView.as_view(), name = 'detail_blog'),

]