from django.contrib import admin

# Register your models here.
from .models import Offer,OfferDetail
from .forms import OfferForm, OfferDetailForm

class OfferAdmin(admin.ModelAdmin):
    model = Offer
    form = OfferForm


class OfferDetailAdmin(admin.ModelAdmin):
    model = OfferDetail
    form = OfferDetailForm


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)
