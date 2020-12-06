from django.contrib import admin

from .actions import make_draft, make_published

# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    actions = [make_draft, make_published]
