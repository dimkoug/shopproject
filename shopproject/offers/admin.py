from django.contrib import admin

# Register your models here.

from .models import Offer, OfferProduct
from .forms import OfferForm

class OfferProductInline(admin.TabularInline):
    model = OfferProduct
    extra = 1
    fk_name = 'offer'
    autocomplete_fields = ['product']


class OfferAdmin(admin.ModelAdmin):
    model = Offer
    form = OfferForm
    search_fields = ['name']

    inlines = [
        OfferProductInline
    ]


admin.site.register(Offer, OfferAdmin)