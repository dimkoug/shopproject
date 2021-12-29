from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Prefetch

from core.views import (
    BaseIndexView, BaseListView, BaseDetailView,
    BaseCreateView, BaseUpdateView, BaseDeleteView
)

from core.mixins import FormMixin, SuccessUrlMixin


from .models import (
    Category, ChildCategory, Tag, Supplier, WareHouse, Brand, BrandSupplier,
    Feature, FeatureCategory, Attribute, Product, ProductCategory,
    ProductTag, ProductRelated, Media, Logo, Stock, Shipment,
    ProductAttribute, Hero, HeroItem, Offer, OfferProduct, ShoppingCart,
    Address, Order, OrderItem
)


from .forms import (
    CategoryForm, ChildCategoryForm, ChildCategoryFormSet,
    TagForm, SupplierForm, WareHouseForm, BrandForm,
    SupplierFormSet, FeatureForm, CategoryFormSet, AttributeForm,
    ProductForm, ProductCategoryFormSet, ProductTagFormSet,
    ProductRelatedFormSet, MediaForm, LogoForm, StockForm, ShipmentForm,
    ProductAttributeFormSet, HeroForm, HeroItemFormSet, OfferForm,
    OfferProductFormSet, AddressForm, OrderForm, OrderItemFormSet,
    MediaFormSet, LogoFormSet, StockFormSet, AttributeFeatureForm,
    AttributeFeatureFormSet
)


class IndexView(LoginRequiredMixin, BaseIndexView):
    app = 'shop'


class CategoryListView(LoginRequiredMixin, BaseListView):
    model = Category
    queryset = Category.objects.prefetch_related('children')


class CategoryDetailView(LoginRequiredMixin, BaseDetailView):
    model = Category


class CategoryCreateView(LoginRequiredMixin, FormMixin,
                         SuccessUrlMixin, BaseCreateView):
    model = Category
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Child Categories',
                'formset': ChildCategoryFormSet(self.request.POST or None)
            }
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                ChildCategoryFormSet(self.request.POST, instance=obj)
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, FormMixin,
                         SuccessUrlMixin, BaseUpdateView):
    model = Category
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Child Categories',
                'formset': ChildCategoryFormSet(self.request.POST or None,
                                                instance=self.get_object())
            }
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                ChildCategoryFormSet(self.request.POST, instance=obj)
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Category


class TagListView(LoginRequiredMixin, BaseListView):
    model = Tag


class TagDetailView(LoginRequiredMixin, BaseDetailView):
    model = Tag


class TagCreateView(LoginRequiredMixin, FormMixin,
                    SuccessUrlMixin, BaseCreateView):
    model = Tag
    form_class = TagForm


class TagUpdateView(LoginRequiredMixin, FormMixin,
                    SuccessUrlMixin, BaseUpdateView):
    model = Tag
    form_class = TagForm


class TagDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Tag


class SupplierListView(LoginRequiredMixin, BaseListView):
    model = Supplier


class SupplierDetailView(LoginRequiredMixin, BaseDetailView):
    model = Supplier


class SupplierCreateView(LoginRequiredMixin, FormMixin,
                         SuccessUrlMixin, BaseCreateView):
    model = Supplier
    form_class = SupplierForm


class SupplierUpdateView(LoginRequiredMixin, FormMixin,
                         SuccessUrlMixin, BaseUpdateView):
    model = Supplier
    form_class = SupplierForm


class SupplierDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Supplier


class WareHouseListView(LoginRequiredMixin, BaseListView):
    model = WareHouse


class WareHouseDetailView(LoginRequiredMixin, BaseDetailView):
    model = WareHouse


class WareHouseCreateView(LoginRequiredMixin, FormMixin,
                          SuccessUrlMixin, BaseCreateView):
    model = WareHouse
    form_class = WareHouseForm


class WareHouseUpdateView(LoginRequiredMixin, FormMixin,
                          SuccessUrlMixin, BaseUpdateView):
    model = WareHouse
    form_class = WareHouseForm


class WareHouseDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = WareHouse


class BrandListView(LoginRequiredMixin, BaseListView):
    model = Brand
    queryset = Brand.objects.prefetch_related('suppliers')


class BrandDetailView(LoginRequiredMixin, BaseDetailView):
    model = Brand


class BrandCreateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseCreateView):
    model = Brand
    form_class = BrandForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Suppliers',
                'formset': SupplierFormSet(self.request.POST or None)
            }
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                SupplierFormSet(self.request.POST, instance=obj)
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class BrandUpdateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseUpdateView):
    model = Brand
    form_class = BrandForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Suppliers',
                'formset': SupplierFormSet(self.request.POST or None,
                                           instance=self.get_object())
            }
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                SupplierFormSet(self.request.POST, instance=obj)
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class BrandDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Brand


class FeatureListView(LoginRequiredMixin, BaseListView):
    model = Feature
    queryset = Feature.objects.prefetch_related('categories')


class FeatureDetailView(LoginRequiredMixin, BaseDetailView):
    model = Feature


class FeatureCreateView(LoginRequiredMixin, FormMixin,
                        SuccessUrlMixin, BaseCreateView):
    model = Feature
    form_class = FeatureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Categories',
                'formset': CategoryFormSet(self.request.POST or None)
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                CategoryFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class FeatureUpdateView(LoginRequiredMixin, FormMixin,
                        SuccessUrlMixin, BaseUpdateView):
    model = Feature
    form_class = FeatureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Categories',
                'formset': CategoryFormSet(self.request.POST or None,
                                           instance=self.get_object())
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                CategoryFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class FeatureDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Feature


class AttributeListView(LoginRequiredMixin, BaseListView):
    model = Attribute
    queryset = Attribute.objects.prefetch_related('features')


class AttributeDetailView(LoginRequiredMixin, BaseDetailView):
    model = Attribute


class AttributeCreateView(LoginRequiredMixin, FormMixin,
                          SuccessUrlMixin, BaseCreateView):
    model = Attribute
    form_class = AttributeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Features',
                'formset': AttributeFeatureFormSet(self.request.POST or None)
            }
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                AttributeFeatureFormSet(self.request.POST, instance=obj)
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class AttributeUpdateView(LoginRequiredMixin, FormMixin,
                          SuccessUrlMixin, BaseUpdateView):
    model = Attribute
    form_class = AttributeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Features',
                'formset': AttributeFeatureFormSet(self.request.POST or None, instance=self.get_object())
            }
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                AttributeFeatureFormSet(self.request.POST, instance=obj)
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class AttributeDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Attribute


class ProductListView(LoginRequiredMixin, BaseListView):
    model = Product


class ProductDetailView(LoginRequiredMixin, BaseDetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, FormMixin,
                        SuccessUrlMixin, BaseCreateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Product Categories',
                'formset': ProductCategoryFormSet(
                        self.request.POST or None,
                        queryset=ProductCategory.objects.select_related(
                            'product', 'category'))
            },
            {
                'title': 'Product Tags',
                'formset': ProductTagFormSet(
                        self.request.POST or None,
                        queryset=ProductTag.objects.select_related(
                            'product', 'tag'))
            },
            {
                'title': 'Product Attributes',
                'formset': ProductAttributeFormSet(
                        self.request.POST or None,
                        queryset=ProductAttribute.objects.select_related(
                            'product', 'attribute'))
            },
            {
                'title': 'Related Products',
                'formset': ProductRelatedFormSet(
                        self.request.POST or None,
                        queryset=ProductRelated.objects.select_related(
                            'source', 'target'))
            },
            {
                'title': 'Media',
                'formset': MediaFormSet(
                        self.request.POST or None, self.request.FILES or None,
                        queryset=Media.objects.select_related('product'))
            },
            {
                'title': 'Logo',
                'formset': LogoFormSet(
                        self.request.POST or None, self.request.FILES or None,
                        queryset=Logo.objects.select_related('product'))
            },
            {
                'title': 'Stock',
                'formset': StockFormSet(
                        self.request.POST or None, self.request.FILES or None,
                        queryset=Stock.objects.select_related(
                            'product', 'warehouse'))
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                ProductCategoryFormSet(self.request.POST, instance=obj),
                ProductAttributeFormSet(self.request.POST, instance=obj),
                ProductTagFormSet(self.request.POST, instance=obj),
                ProductRelatedFormSet(self.request.POST, instance=obj),
                MediaFormSet(self.request.POST, self.request.FILES,
                             instance=obj),
                LogoFormSet(self.request.POST, self.request.FILES,
                            instance=obj),
                StockFormSet(self.request.POST, self.request.FILES,
                             instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, FormMixin,
                        SuccessUrlMixin, BaseUpdateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Product Categories',
                'formset': ProductCategoryFormSet(
                        self.request.POST or None, instance=self.get_object(),
                        queryset=ProductCategory.objects.select_related(
                            'product', 'category'))
            },
            {
                'title': 'Product Tags',
                'formset': ProductTagFormSet(
                        self.request.POST or None, instance=self.get_object(),
                        queryset=ProductTag.objects.select_related(
                            'product', 'tag'))
            },
            {
                'title': 'Product Attributes',
                'formset': ProductAttributeFormSet(
                        self.request.POST or None, instance=self.get_object(),
                        queryset=ProductAttribute.objects.select_related(
                            'product', 'attribute'))
            },
            {
                'title': 'Related Products',
                'formset': ProductRelatedFormSet(
                        self.request.POST or None, instance=self.get_object(),
                        queryset=ProductRelated.objects.select_related(
                            'source', 'target'))
            },
            {
                'title': 'Media',
                'formset': MediaFormSet(
                        self.request.POST or None, self.request.FILES or None,
                        instance=self.get_object(),
                        queryset=Media.objects.select_related('product'))
            },
            {
                'title': 'Logo',
                'formset': LogoFormSet(
                        self.request.POST or None, self.request.FILES or None,
                        instance=self.get_object(),
                        queryset=Logo.objects.select_related('product'))
            },
            {
                'title': 'Stock',
                'formset': StockFormSet(
                        self.request.POST or None, self.request.FILES or None,
                        instance=self.get_object(),
                        queryset=Stock.objects.select_related(
                            'product', 'warehouse'))
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                ProductCategoryFormSet(self.request.POST, instance=obj),
                ProductAttributeFormSet(self.request.POST, instance=obj),
                ProductTagFormSet(self.request.POST, instance=obj),
                ProductRelatedFormSet(self.request.POST, instance=obj),
                MediaFormSet(self.request.POST, self.request.FILES,
                             instance=obj),
                LogoFormSet(self.request.POST, self.request.FILES,
                            instance=obj),
                StockFormSet(self.request.POST, self.request.FILES,
                             instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Product


class MediaListView(LoginRequiredMixin, BaseListView):
    model = Media


class MediaDetailView(LoginRequiredMixin, BaseDetailView):
    model = Media


class MediaCreateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseCreateView):
    model = Media
    form_class = MediaForm


class MediaUpdateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseUpdateView):
    model = Media
    form_class = MediaForm


class MediaDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Media


class LogoListView(LoginRequiredMixin, BaseListView):
    model = Logo


class LogoDetailView(LoginRequiredMixin, BaseDetailView):
    model = Logo


class LogoCreateView(LoginRequiredMixin, FormMixin,
                     SuccessUrlMixin, BaseCreateView):
    model = Logo
    form_class = LogoForm


class LogoUpdateView(LoginRequiredMixin, FormMixin,
                     SuccessUrlMixin, BaseUpdateView):
    model = Logo
    form_class = LogoForm


class LogoDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Logo


class StockListView(LoginRequiredMixin, BaseListView):
    model = Stock


class StockDetailView(LoginRequiredMixin, BaseDetailView):
    model = Stock


class StockCreateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseCreateView):
    model = Stock
    form_class = StockForm


class StockUpdateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseUpdateView):
    model = Stock
    form_class = StockForm


class StockDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Stock


class ShipmentListView(LoginRequiredMixin, BaseListView):
    model = Shipment


class ShipmentDetailView(LoginRequiredMixin, BaseDetailView):
    model = Shipment


class ShipmentCreateView(LoginRequiredMixin, FormMixin,
                          SuccessUrlMixin, BaseCreateView):
    model = Shipment
    form_class = ShipmentForm


class ShipmentUpdateView(LoginRequiredMixin, FormMixin,
                          SuccessUrlMixin, BaseUpdateView):
    model = Shipment
    form_class = ShipmentForm


class ShipmentDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Shipment


class HeroListView(LoginRequiredMixin, BaseListView):
    model = Hero


class HeroDetailView(LoginRequiredMixin, BaseDetailView):
    model = Hero


class HeroCreateView(LoginRequiredMixin, FormMixin,
                     SuccessUrlMixin, BaseCreateView):
    model = Hero
    form_class = HeroForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Items',
                'formset': HeroItemFormSet(self.request.POST or None)
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                HeroItemFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class HeroUpdateView(LoginRequiredMixin, FormMixin,
                     SuccessUrlMixin, BaseUpdateView):
    model = Hero
    form_class = HeroForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Items',
                'formset': HeroItemFormSet(self.request.POST or None,
                                           instance=self.get_object())
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                HeroItemFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class HeroDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Hero


class OfferListView(LoginRequiredMixin, BaseListView):
    model = Offer


class OfferDetailView(LoginRequiredMixin, BaseDetailView):
    model = Offer


class OfferCreateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseCreateView):
    model = Offer
    form_class = OfferForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Items',
                'formset': OfferProductFormSet(self.request.POST or None)
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                OfferProductFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class OfferUpdateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseUpdateView):
    model = Offer
    form_class = OfferForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Items',
                'formset': OfferProductFormSet(self.request.POST or None,
                                               instance=self.get_object())
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                OfferProductFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class OfferDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Offer


class AddressListView(LoginRequiredMixin, BaseListView):
    model = Address


class AddressDetailView(LoginRequiredMixin, BaseDetailView):
    model = Address


class AddressCreateView(LoginRequiredMixin, FormMixin,
                        SuccessUrlMixin, BaseCreateView):
    model = Address
    form_class = AddressForm


class AddressUpdateView(LoginRequiredMixin, FormMixin,
                        SuccessUrlMixin, BaseUpdateView):
    model = Address
    form_class = AddressForm


class AddressDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Address


class OrderListView(LoginRequiredMixin, BaseListView):
    model = Order


class OrderDetailView(LoginRequiredMixin, BaseDetailView):
    model = Order


class OrderCreateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseCreateView):
    model = Order
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Items',
                'formset': OrderItemFormSet(self.request.POST or None)
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                OrderItemFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseUpdateView):
    model = Order
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Items',
                'formset': OrderItemFormSet(self.request.POST or None,
                                            instance=self.get_object())
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                OrderItemFormSet(self.request.POST, instance=obj),
            ]
            for formset in formsets:
                if formset.is_valid():
                    obj.save()
                    formset.save()
                else:
                    print(formset.non_form_errors())
                    print("formset errors:", formset.errors)
                    return super().form_invalid(form)
        return super().form_valid(form)


class OrderDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Order
