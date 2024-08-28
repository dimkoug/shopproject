from django import forms

from core.forms import BootstrapForm
from core.widgets import CustomSelectMultipleWithUrl, CustomSelectWithQueryset

from suppliers.models import Supplier

from .models import Brand

class BrandForm(BootstrapForm, forms.ModelForm):
    suppliers = forms.ModelMultipleChoiceField(widget=CustomSelectMultipleWithUrl(ajax_url='/suppliers/sb/'),required=False,queryset=Supplier.objects.none())
    class Meta:
        model = Brand
        fields = ('name', 'image','suppliers',)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        if 'suppliers' in self.data:
            queryset = Supplier.objects.all()
            self.fields['suppliers'].queryset = queryset
            self.fields['suppliers'].widget.queryset = queryset
        else:
            self.fields['suppliers'].queryset = Supplier.objects.none()
            self.fields['suppliers'].widget.queryset = Supplier.objects.none()

      
        
        
        if self.instance.pk:
            supplier_queryset = Supplier.objects.filter(id__in=self.instance.suppliers.all())
            self.fields['suppliers'].queryset = supplier_queryset
            self.fields['suppliers'].widget.queryset = supplier_queryset
