from django.contrib import admin

# Register your models here.
from .models import Hero, HeroItem
from .forms import HeroForm


class HeroAdmin(admin.ModelAdmin):
    model = Hero
    form = HeroForm

admin.site.register(Hero, HeroAdmin)