from django.shortcuts import render, redirect
from django.urls import reverse
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
    Hero,
)


from shop.forms import (
    HeroForm, HeroItemFormSet,
)


class HeroListView(LoginRequiredMixin,CmsListView, BaseListView):
    model = Hero
    paginate_by = 50


class HeroDetailView(LoginRequiredMixin, BaseDetailView):
    model = Hero


class HeroCreateView(LoginRequiredMixin, FormMixin,
                     SuccessUrlMixin, BaseCreateView):
    model = Hero
    form_class = HeroForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Items',
                'formset': HeroItemFormSet(self.request.POST or None),
                "sb_url": reverse("shop:get_products_for_sb")
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                HeroItemFormSet(self.request.POST, instance=obj),
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


class HeroUpdateView(LoginRequiredMixin, FormMixin,
                     SuccessUrlMixin, BaseUpdateView):
    model = Hero
    form_class = HeroForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Items',
                'formset': HeroItemFormSet(self.request.POST or None,
                                           instance=self.get_object()),
                "sb_url": reverse("shop:get_products_for_sb")
            },
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                HeroItemFormSet(self.request.POST, instance=obj),
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


class HeroDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Hero
