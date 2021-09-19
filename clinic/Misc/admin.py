from django.contrib import admin
from .models import Gallery, Blog
from django.utils.html import format_html

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('Title',)
    search_fields = ['title']
    list_display_links = None

    def Title(self,obj):
        return format_html('<a href="/cadmin/Misc/gallery/change/%s">%s</a>' %(obj.id, obj.title))
    Title.allow_tags = True 


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    def thumbnail_tag(self, obj):
        return format_html('<img src = "%s" width = "80" height = "80"/>'%(obj.thumbnail.url))
    thumbnail_tag.short_description = 'Thumbnail'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    list_display = ['title','author','publish_date','status','tag_list']
    search_fields = ['title','author__user__username','tags__name']

    fieldsets = (
        ('General', {
            'fields' : ('title', 'author', 'publish_date', 'tags','thumbnail','status',)
        }),
        ('Content',{
        'fields' : ('content',)
        }),
    )

  
