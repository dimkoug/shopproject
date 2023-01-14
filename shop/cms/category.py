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

from core.functions import is_ajax


from shop.models import (
    Category, ChildCategory
)

from shop.forms import CategoryForm, ChildCategoryForm, ChildCategoryFormSet


class IndexView(LoginRequiredMixin, BaseIndexView):
    app = 'shop'


class CategoryListView(LoginRequiredMixin, BaseListView):
    model = Category
    queryset = Category.objects.prefetch_related('children')
    paginate_by = 50


class CategoryDetailView(LoginRequiredMixin, BaseDetailView):
    model = Category
    queryset = Category.objects.prefetch_related('children')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for c in self.get_object().children.all().order_by('order'):
            print(c, c.order)
        context['categories'] = ChildCategory.objects.select_related('target').filter(source=self.get_object()).order_by('order')
        return context

class CategoryCreateView(LoginRequiredMixin, FormMixin,
                         SuccessUrlMixin, BaseCreateView):
    model = Category
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Child Categories',
                'formset': ChildCategoryFormSet(self.request.POST or None)
            }
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                ChildCategoryFormSet(self.request.POST, instance=obj)
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


class CategoryUpdateView(LoginRequiredMixin, FormMixin,
                         SuccessUrlMixin, BaseUpdateView):
    model = Category
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            {
                'title': 'Child Categories',
                'formset': ChildCategoryFormSet(self.request.POST or None,
                                                instance=self.get_object())
            }
        ]
        return context

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            formsets = [
                ChildCategoryFormSet(self.request.POST, instance=obj)
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


class CategoryDeleteView(LoginRequiredMixin, SuccessUrlMixin, BaseDeleteView):
    model = Category
