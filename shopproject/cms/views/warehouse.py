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

from cms.cms_views import (
    BaseListView, BaseDetailView,
    BaseCreateView, BaseUpdateView, BaseDeleteView
)


from core.functions import is_ajax


from warehouses.models import WareHouse


from  warehouses.forms import WareHouseForm


class WareHouseListView(BaseListView):
    model = WareHouse
    paginate_by = 2
    fields = [
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
    ]


class WareHouseDetailView(BaseDetailView):
    model = WareHouse


class WareHouseCreateView(BaseCreateView):
    model = WareHouse
    form_class = WareHouseForm


class WareHouseUpdateView(BaseUpdateView):
    model = WareHouse
    form_class = WareHouseForm


class WareHouseDeleteView(BaseDeleteView):
    model = WareHouse
