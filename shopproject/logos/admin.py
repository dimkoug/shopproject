from django.contrib import admin

# Register your models here.
from .models import Logo
from .forms import LogoForm

class LogoAdmin(admin.ModelAdmin):
    model = Logo
    form = LogoForm

admin.site.register(Logo, LogoAdmin)