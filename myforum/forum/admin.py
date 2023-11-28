from django.contrib import admin
from django.utils.html import mark_safe
from .models import Tag, Image

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_display', 'tag_list')

    def image_display(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" height="50" />')
    image_display.short_description = 'Image'

    def tag_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tag_list.short_description = 'Tags'

admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
