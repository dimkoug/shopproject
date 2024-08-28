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


from offers.models import Offer


from offers.forms import OfferForm


class OfferListView(BaseListView):
    model = Offer
    paginate_by = 50
    fields = [
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
    ]


class OfferDetailView(BaseDetailView):
    model = Offer


class OfferCreateView(BaseCreateView):
    model = Offer
    form_class = OfferForm

class OfferUpdateView(BaseUpdateView):
    model = Offer
    form_class = OfferForm

class OfferDeleteView(BaseDeleteView):
    model = Offer
