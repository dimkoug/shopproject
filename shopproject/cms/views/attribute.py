from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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

from shop.models import Attribute


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


def create_attribute(request):
    try:
        feature_id = request.POST['feature']
        attribute = request.POST['name']
        product_attribute, created = Attribute.objects.get_or_create(feature_id=feature_id,name=attribute)
        return JsonResponse({
            'id':product_attribute.id,
            'feature':product_attribute.feature_id,
            'name': product_attribute.name,
        })
    except Exception as e:
        print(e)
        return JsonResponse({})

def delete_attribute(request):
    try:
        feature_id = request.POST['feature']
        attribute = request.POST['attribute']
        product_attribute = Attribute.objects.get(feature_id=feature_id,id=attribute)
        product_attribute.delete()
    except:
        pass
    return JsonResponse({})