from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Prefetch
from django.shortcuts import render
from django.apps import apps

from core.views import (
    BaseIndexView, BaseListView, BaseDetailView,
    BaseCreateView, BaseUpdateView, BaseDeleteView
)

from core.mixins import FormMixin, SuccessUrlMixin
from cms.views.core import CmsListView

from core.functions import is_ajax


from shop.models import (
    Feature,
    FeatureCategory
)


from cms.forms import (
    FeatureForm, CategoryFormSet
)


class FeatureListView(LoginRequiredMixin,CmsListView, BaseListView):
    model = Feature
    queryset = Feature.objects.prefetch_related('categories').order_by('order')
    paginate_by = 20
    fields = [
        {
        'verbose_name': 'Feature',
        'db_name':'name'
        },
        {
            'verbose_name': 'Order',
            'db_name': 'order'
        },
        {
        'verbose_name': 'Categories',
        'db_name':'categories'
        },
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        print(category)
        if category and category != '':
            queryset = queryset.filter(categories=category)
        return queryset


class FeatureDetailView(LoginRequiredMixin, BaseDetailView):
    model = Feature


class FeatureCreateView(LoginRequiredMixin, FormMixin,
                        SuccessUrlMixin, BaseCreateView):
    model = Feature
    form_class = FeatureForm

class FeatureUpdateView(LoginRequiredMixin, FormMixin,
                        SuccessUrlMixin, BaseUpdateView):
    model = Feature
    form_class = FeatureForm


class FeatureDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Feature


def create_featurecategory(request):
    try:
        feature_id = request.POST['feature']
        category_id = request.POST['category']
        filter_display = bool(request.POST.get('filter_display'))
        product_attribute, created = FeatureCategory.objects.update_or_create(feature_id=feature_id,category_id=category_id,defaults={"filter_display":filter_display})
        return JsonResponse({
            'id':product_attribute.id,
            'feature':product_attribute.feature_id,
            'category': product_attribute.category.name,
            'category_id': product_attribute.category_id,
            'filter_display':product_attribute.filter_display
        })
    except Exception as e:
        print(e)
        raise
        return JsonResponse({})

def delete_featurecategory(request):
    try:
        feature_id = request.POST['feature']
        category_id = request.POST['category']
        FeatureCategory.objects.filter(feature_id=feature_id,category_id=category_id).delete()
    except:
        raise
    return JsonResponse({})