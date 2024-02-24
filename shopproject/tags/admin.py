from django.contrib import admin

# Register your models here.

from .models import Tag
from .forms import TagForm


class TagAdmin(admin.ModelAdmin):
    model = Tag
    form = TagForm
    search_fields = ['name']



admin.site.register(Tag, TagAdmin)