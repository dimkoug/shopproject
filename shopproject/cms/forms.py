from django import forms
from django.forms import inlineformset_factory

from core.forms import BootstrapForm, BootstrapFormSet

from tags.models import Tag
from brands.models import Brand
from stocks.models import Stock

from stocks.forms import StockForm

from shop.models import (
    Category, ChildCategory,
    Feature, FeatureCategory, Attribute, Product,
    ProductTag, ProductRelated, Media, ProductLogo,
    ProductAttribute,
)


class CategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'image', 'is_published', 'order', 'children')


class ChildCategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ChildCategory
        fields = ('source', 'target', 'order')


ChildCategoryFormSet = inlineformset_factory(Category, ChildCategory,
                                             form=ChildCategoryForm,
                                             formset=BootstrapFormSet,
                                             can_delete=True,
                                             fk_name='source')




class FeatureForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Feature
        fields = ('name', 'image','is_published', 'order')


class FeatureCategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = FeatureCategory
        fields = ('feature', 'category',)


CategoryFormSet = inlineformset_factory(Feature, FeatureCategory,
                                        form=FeatureCategoryForm,
                                        formset=BootstrapFormSet,
                                        can_delete=True,
                                        fk_name='feature')


class AttributeForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ('name', 'is_published', 'feature', 'order')


AttributeFormSet = inlineformset_factory(Feature, Attribute,
                                         form=AttributeForm,
                                         formset=BootstrapFormSet,
                                         can_delete=True,
                                         fk_name='feature')


class ProductForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'brand','category', 'parent', 'image', 'subtitle',
                  'description', 'price', 'is_published', 'order')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.none()
        self.fields['brand'].widget=forms.Select(attrs={'class': 'form-control'})
        self.fields['parent'].queryset = Product.objects.none()
        self.fields['parent'].widget=forms.Select(attrs={'class': 'form-control'})
        self.fields['category'].queryset = Category.objects.none()
        self.fields['category'].widget=forms.Select(attrs={'class': 'form-control'})

        if 'brand' in self.data:
            self.fields['brand'].queryset = Brand.objects.all()

        if 'category' in self.data:
            self.fields['category'].queryset = Category.objects.all()
        
        if 'parent' in self.data:
            self.fields['parent'].queryset = Product.objects.all()

        if self.instance.pk:
            self.fields['brand'].queryset = Brand.objects.filter(id=self.instance.brand_id)
            self.fields['parent'].queryset = Product.objects.filter(id=self.instance.parent_id)
            self.fields['category'].queryset = Category.objects.filter(id=self.instance.category_id)


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


ProductTagFormSet = inlineformset_factory(Product, ProductTag,
                                          form=ProductTagForm,
                                          formset=BootstrapFormSet,
                                          can_delete=True,
                                          fk_name='product')


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


ProductRelatedFormSet = inlineformset_factory(Product, ProductRelated,
                                              form=ProductRelatedForm,
                                              formset=BootstrapFormSet,
                                              can_delete=True,
                                              fk_name='source'
                                              )


class MediaForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Media
        fields = ('product', 'image', 'is_published', 'order')



MediaFormSet = inlineformset_factory(Product, Media,
                                     form=MediaForm,
                                     formset=BootstrapFormSet,
                                     can_delete=True,
                                     fk_name='product')


class ProductLogoForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = ProductLogo
        fields = ('product', 'logo')


ProductLogoFormSet = inlineformset_factory(Product, ProductLogo,
                                    form=ProductLogoForm,
                                    formset=BootstrapFormSet,
                                    can_delete=True,
                                    fk_name='product')





StockFormSet = inlineformset_factory(Product, Stock,
                                     form=StockForm,
                                     formset=BootstrapFormSet,
                                     can_delete=True,
                                     fk_name='product')




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


ProductAttributeFormSet = inlineformset_factory(Product, ProductAttribute,
                                                form=ProductAttributeForm,
                                                formset=BootstrapFormSet,
                                                can_delete=True,
                                                fk_name='product')



