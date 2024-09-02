import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.shortcuts import render
from django.apps import apps

from cms.cms_views import (
    BaseListView, BaseDetailView,
    BaseCreateView, BaseUpdateView, BaseDeleteView
)

from shop.models import Attribute, Product,Feature, ProductAttribute


from cms.forms import AttributeForm


class AttributeListView(BaseListView):
    model = Attribute
    queryset = Attribute.objects.select_related('feature')
    paginate_by = 20
    fields = [
        {
        'verbose_name': 'Feature',
        'db_name':'feature'
        },
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        feature = self.request.GET.get('feature')
        if feature and feature != '':
            queryset = queryset.filter(feature_id=feature)
        return queryset


class AttributeDetailView(BaseDetailView):
    model = Attribute


class AttributeCreateView(BaseCreateView):
    model = Attribute
    form_class = AttributeForm


class AttributeUpdateView(BaseUpdateView):
    model = Attribute
    form_class = AttributeForm


class AttributeDeleteView(BaseDeleteView):
    model = Attribute


def create_attribute(request,product_id):
    context = {}
    template_name = 'cms/shop/add_attribute.html'
    product = Product.objects.get(id=product_id)
    features = Feature.objects.filter(categories=product.category_id).distinct()
    context['features'] = features
    context['product'] = product
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST['product_id'])
        feature = Feature.objects.get(id=request.POST['feature'])
        str2hash = f"{feature.name}{request.POST['value']}"
        result = hashlib.md5(str2hash.encode())
        attribute_hash = result.hexdigest()
        ProductAttribute.objects.filter(attribute__feature_id=feature.id,product=product).delete()
        attribute,_ = Attribute.objects.get_or_create(feature=feature,value=request.POST['value'],hash=attribute_hash)
        ProductAttribute.objects.get_or_create(product=product,attribute=attribute)
        return redirect(reverse("cms:product-update",kwargs={"pk":product.id}))
    return render(request,template_name,context)


def delete_attribute(request):
    try:
        feature_id = request.POST['feature']
        attribute = request.POST['attribute']
        product_attribute = Attribute.objects.get(feature_id=feature_id,id=attribute)
        product_attribute.delete()
    except:
        pass
    return JsonResponse({})