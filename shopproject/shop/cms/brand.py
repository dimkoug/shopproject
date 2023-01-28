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
    Brand,
)


from shop.forms import (
    BrandForm,
    SupplierFormSet,
)


class BrandListView(LoginRequiredMixin,CmsListView, BaseListView):
    model = Brand
    queryset = Brand.objects.prefetch_related('suppliers')
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        supplier = self.request.GET.get('supplier')
        if supplier and supplier != '':
            queryset = queryset.filter(suppliers=supplier)
        return queryset


class BrandDetailView(LoginRequiredMixin, BaseDetailView):
    model = Brand


class BrandCreateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseCreateView):
    model = Brand
    form_class = BrandForm

class BrandUpdateView(LoginRequiredMixin, FormMixin,
                      SuccessUrlMixin, BaseUpdateView):
    model = Brand
    form_class = BrandForm

class BrandDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Brand
