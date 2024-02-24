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

from core.mixins import FormMixin, SuccessUrlMixin, PaginationMixin
from cms.views.core import CmsListView


from core.functions import is_ajax


from addresses.models import (
    Address,
)


from addresses.forms import (
    AddressForm,
)


class AddressListView(LoginRequiredMixin,CmsListView, BaseListView):
    model = Address
    paginate_by = 50
    fields = [
        {
        'verbose_name': 'First Name',
        'db_name':'first_name'
        },
        {
        'verbose_name': 'Last Name',
        'db_name':'last_name'
        },
        {
        'verbose_name': 'Mobile',
        'db_name':'mobile'
        },
    ]


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
