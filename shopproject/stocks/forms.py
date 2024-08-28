from django import forms

from core.forms import BootstrapForm
from core.widgets import *

from shop.models import Product
from warehouses.models import Warehouse


from stocks.models import Stock


class StockForm(BootstrapForm, forms.ModelForm):
    warehouse = forms.ModelChoiceField(widget=CustomSelectWithQueryset(ajax_url='/warehouses/sb/'),required=False,queryset=Warehouse.objects.none())
    product = forms.ModelChoiceField(widget=CustomSelectWithQueryset(ajax_url='/products/sb/'),required=False,queryset=Product.objects.none())
    class Meta:
        model = Stock
        fields = ('warehouse','product', 'stock')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        warehouse_queryset = Warehouse.objects.none()
        products_queryset = Product.objects.none()
        if 'warehouse' in self.data:
            warehouse_queryset = Warehouse.objects.all()

        if 'product' in self.data:
            products_queryset = Product.objects.all()

        if self.instance.pk:
            warehouse_queryset = Warehouse.objects.filter(id=self.instance.warehouse_id)
            products_queryset = Product.objects.filter(id=self.instance.product_id)

        self.fields['warehouse'].queryset = warehouse_queryset
        self.fields['warehouse'].widget.queryset = warehouse_queryset


        self.fields['product'].queryset = products_queryset
        self.fields['product'].widget.queryset = products_queryset
