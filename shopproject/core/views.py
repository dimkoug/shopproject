from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .mixins import ModelMixin, PaginationMixin



class BaseIndexView(TemplateView):
    def get_template_names(self):
        return ['{}/cms/index.html'.format(
                self.app)]


class BaseListView(ModelMixin, PaginationMixin, ListView):
    def get_template_names(self):
        return ['{}/cms/{}_list.html'.format(
                self.model._meta.app_label, self.model.__name__)]
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            context['fields'] = self.fields
        except:
            raise
        
        return context


class BaseDetailView(ModelMixin, DetailView):
    def get_template_names(self):
        return ['{}/cms/{}_detail.html'.format(
                self.model._meta.app_label, self.model.__name__)]


class BaseCreateView(ModelMixin, CreateView):
    def get_template_names(self):
        return ['{}/cms/{}_form.html'.format(
                self.model._meta.app_label, self.model.__name__)]


class BaseUpdateView(ModelMixin, UpdateView):
    def get_template_names(self):
        return ['{}/cms/{}_form.html'.format(
                self.model._meta.app_label, self.model.__name__)]


class BaseDeleteView(ModelMixin, DeleteView):
    def get_template_names(self):
        return ['{}/cms/{}_confirm_delete.html'.format(
                self.model._meta.app_label, self.model.__name__)]
