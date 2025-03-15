from django.contrib import admin
from django.utils.html import format_html
from .actions import make_draft, make_published
from .forms import AdminImageWidget


class ImageAdminMixin(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.__class__.__name__ == 'ImageField':
            request = kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super().formfield_for_dbfield(
            db_field, **kwargs)


# Register your models here.

class BaseAdmin(ImageAdminMixin, admin.ModelAdmin):
    def admin_thumbnail(self):
        if(self.image):
            return format_html('<img src="{}">'.format(self.image.url))
        return ""
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

    list_display = [admin_thumbnail]
    actions = [make_draft, make_published]
