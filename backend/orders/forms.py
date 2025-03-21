from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from addresses.models import Address


from .models import Order, OrderItem


class OrderForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_registration', 'billing_address', 'shipping_address',
                  'total', 'comments')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)


class SiteOrderForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Order
        fields = ('billing_address', 'shipping_address',
                  'comments')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['billing_address'].queryset = Address.objects.select_related(
            'profile').filter(profile_id=self.request.user.profile.pk,
                              address_type=Address.BILLING_ADDRESS)
        self.fields['shipping_address'].queryset = Address.objects.select_related(
            'profile').filter(profile_id=self.request.user.profile.pk,
                              address_type=Address.SHIPPING_ADDRESS)


class OrderItemForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('order', 'product', 'quantity')


OrderItemFormSet = inlineformset_factory(Order, OrderItem,
                                         form=OrderItemForm,
                                         formset=BootstrapFormSet,
                                         can_delete=True,
                                         fk_name='order')