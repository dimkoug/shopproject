from django.contrib import admin

# Register your models here.
from .models import Hero, HeroItem
from .forms import HeroForm, HeroItemFormSet


class HeroItemInline(admin.TabularInline):
    model = HeroItem
    formset = HeroItemFormSet
    fk_name = 'hero'
    extra = 1
    autocomplete_fields = ['product']

class HeroAdmin(admin.ModelAdmin):
    model = Hero
    form = HeroForm

    inlines = [
        HeroItemInline,
    ]


admin.site.register(Hero, HeroAdmin)