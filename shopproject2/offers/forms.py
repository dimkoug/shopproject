from django import forms
from core.forms import BootstrapForm

from .models import Offer, OfferDetail

class OfferForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('name','start_date','end_date', 'is_published')


class OfferDetailForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = OfferDetail
        fields = ('offer', 'product','price')
