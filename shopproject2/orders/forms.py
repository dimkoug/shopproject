from django import forms
from core.forms import BootstrapForm

from .models import Order, OrderDetail

class OrderForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = Order
        fields = ('profile', 'amount')
        widgets = {'amount': forms.HiddenInput(), 'profile': forms.HiddenInput()}


class OrderDetailForm(BootstrapForm,forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ('order', 'product', 'quantity')
