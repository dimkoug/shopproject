from django.contrib import admin
from django.utils.html import format_html

from .actions import make_draft, make_published

# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    def admin_thumbnail(self):
        if(self.image):
            return format_html(u'<img src="%s" style="width:50px"/>' % (self.image.url))
        return ""
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True
    list_display = [admin_thumbnail]
    actions = [make_draft, make_published]
