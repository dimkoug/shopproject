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
from shop.cms.core import CmsListView

from core.functions import is_ajax


from shop.models import (
    Feature,
)


from shop.forms import (
    FeatureForm, CategoryFormSet
)


class FeatureListView(LoginRequiredMixin,CmsListView, BaseListView):
    model = Feature
    queryset = Feature.objects.prefetch_related('categories')
    paginate_by = 20
    fields = [
        {
        'verbose_name': 'Feature',
        'db_name':'name'
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
