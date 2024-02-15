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
    Offer,
)


from cms.forms import (
    OfferForm,
    OfferProductFormSet,
)


class OfferListView(LoginRequiredMixin,CmsListView, BaseListView):
    model = Offer
    paginate_by = 50
    fields = [
        {
        'verbose_name': 'Name',
        'db_name':'name'
        },
    ]


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
