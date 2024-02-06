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
    Shipment,
)


from shop.forms import (
    ShipmentForm,

)


class ShipmentListView(LoginRequiredMixin,CmsListView, BaseListView):
    model = Shipment
    paginate_by = 50
    fields = [
        {
        'verbose_name': 'Warehouse',
        'db_name':'warehouse'
        },
        {
        'verbose_name': 'Product',
        'db_name':'product'
        },
        {
        'verbose_name': 'stock',
        'db_name':'stock'
        },
    ]


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
