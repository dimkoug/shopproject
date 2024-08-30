from django import forms
from django.forms import inlineformset_factory

from core.widgets import CustomSelectMultipleWithUrl, CustomSelectWithQueryset
from core.forms import BootstrapForm, BootstrapFormSet

from tags.models import Tag
from brands.models import Brand
from stocks.models import Stock

from shop.models import (
    Category,
    Feature, FeatureCategory, Attribute, Product,
    ProductTag, ProductRelated, ProductMedia, ProductLogo,
    ProductAttribute,
)


class CategoryForm(BootstrapForm, forms.ModelForm):
    children = forms.ModelMultipleChoiceField(widget=CustomSelectMultipleWithUrl(ajax_url='/shop/categories/sb/'),required=False,queryset=Category.objects.none())
    class Meta:
        model = Category
        fields = ('name', 'image', 'is_published', 'order', 'children')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        queryset = Category.objects.none()
        if 'children' in self.data:
            queryset = Category.objects.all()
    
        if self.instance.pk:
            queryset = Category.objects.filter(id__in=self.instance.children.all())
        self.fields['children'].queryset = queryset
        self.fields['children'].widget.queryset = queryset



class FeatureForm(BootstrapForm, forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(widget=CustomSelectMultipleWithUrl(ajax_url='/shop/categories/sb/'),required=False,queryset=Category.objects.none())
    class Meta:
        model = Feature
        fields = ('name','categories', 'image','is_published', 'order')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        queryset = Category.objects.none()
        if 'categories' in self.data:
            queryset = Category.objects.all()
    
        if self.instance.pk:
            queryset = Category.objects.filter(id__in=self.instance.categories.all())
        self.fields['categories'].queryset = queryset
        self.fields['categories'].widget.queryset = queryset


class AttributeForm(BootstrapForm, forms.ModelForm):
    feature = forms.ModelChoiceField(widget=CustomSelectWithQueryset(ajax_url='/shop/features/sb/'),required=False,queryset=Feature.objects.none())
    class Meta:
        model = Attribute
        fields = ('name', 'is_published', 'feature', 'order')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        feature_queryset = Feature.objects.none()
        if 'feature' in self.data:
            feature_queryset = Feature.objects.all()
    
        if self.instance.pk:
            feature_queryset = Feature.objects.filter(id=self.instance.feature_id)
        self.fields['feature'].queryset = feature_queryset
        self.fields['feature'].widget.queryset = feature_queryset


class ProductForm(BootstrapForm, forms.ModelForm):
    brand = forms.ModelChoiceField(widget=CustomSelectWithQueryset(ajax_url='/brands/sb/'),required=False,queryset=Brand.objects.none())
    category = forms.ModelChoiceField(widget=CustomSelectWithQueryset(ajax_url='/shop/categories/sb/'),required=False,queryset=Category.objects.none())
    parent = forms.ModelChoiceField(widget=CustomSelectWithQueryset(ajax_url='/shop/products/sb/'),required=False,queryset=Product.objects.none())

    class Meta:
        model = Product
        fields = ('name', 'brand','category', 'parent', 'image', 'subtitle',
                  'description', 'price', 'is_published', 'order')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        brand_queryset = Brand.objects.none()
        parent_queryset = Product.objects.none()
        category_queryset = Category.objects.none()
        
        
        if 'brand' in self.data:
            brand_queryset = Brand.objects.all()
        if 'category' in self.data:
            category_queryset = Category.objects.all()
    
        if 'parent' in self.data:
            parent_queryset = Product.objects.all()
           
        
        
        if self.instance.pk:
            brand_queryset = Brand.objects.filter(id=self.instance.brand_id)
            category_queryset = Category.objects.filter(id=self.instance.category_id)
            parent_queryset = Product.objects.filter(id=self.instance.parent_id)


        self.fields['brand'].queryset = brand_queryset
        self.fields['parent'].queryset = parent_queryset
        self.fields['category'].queryset = category_queryset


class ProductTagForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ProductTag
        fields = ('product', 'tag',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.none()
        self.fields['product'].widget=forms.Select(attrs={'class': 'form-control'})
        self.fields['tag'].queryset = Tag.objects.none()
        self.fields['tag'].widget=forms.Select(attrs={'class': 'form-control'})

        if 'product' in self.data:
            self.fields['product'].queryset = Product.objects.all()
        
        if 'tag' in self.data:
            self.fields['tag'].queryset = Tag.objects.all()

        if self.instance.pk:
            self.fields['tag'].queryset = Tag.objects.filter(id=self.instance.tag_id)
            self.fields['product'].queryset = Product.objects.filter(id=self.instance.product_id)


class ProductRelatedForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ProductRelated
        fields = ('source', 'target',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target'].queryset = Product.objects.none()
        self.fields['target'].widget=forms.Select(attrs={'class': 'form-control'})

        if 'target' in self.data:
            self.fields['target'].queryset = Product.objects.all()
        
        if self.instance.pk:
            self.fields['target'].queryset = Product.objects.filter(id=self.instance.target_id)





class ProductMediaForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ProductMedia
        fields = ('product', 'media')



class ProductLogoForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ProductLogo
        fields = ('product', 'logo')



class ProductAttributeForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ('attribute', 'product', 'order')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.none()
        self.fields['product'].widget=forms.Select(attrs={'class': 'form-control'})
        self.fields['attribute'].queryset = Attribute.objects.none()
        self.fields['attribute'].widget=forms.Select(attrs={'class': 'form-control'})

        if 'product' in self.data:
            self.fields['product'].queryset = Product.objects.all()
        
        if 'attribute' in self.data:
            self.fields['attribute'].queryset = Attribute.objects.all()

        if self.instance.pk:
            self.fields['attribute'].queryset = Attribute.objects.filter(id=self.instance.attribute_id)
            self.fields['product'].queryset = Product.objects.filter(id=self.instance.product_id)


