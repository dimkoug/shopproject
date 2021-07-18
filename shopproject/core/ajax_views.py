from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.views import CoreListView, CoreDetailView, CoreCreateView, CoreUpdateView, CoreDeleteView
from core.mixins import AjaxCreateMixin,AjaxUpdateMixin,AjaxDeleteMixin, PassRequestToFormViewMixin, ModelMixin


class CoreAjaxCreateView(LoginRequiredMixin, AjaxCreateMixin,
                         PassRequestToFormViewMixin,
                         ModelMixin, CreateView):
    template = ''
    ajax_partial = ''
    ajax_list_partial = ''
    model_name = ''
    app = ''
    def dispatch(self, *args, **kwargs):
        self.template = 'form'
        self.app = self.model._meta.app_label
        self.model_name = self.model.__name__.lower()
        self.ajax_partial = '{}/partials/{}_form_partial.html'.format(self.app,self.model_name)
        self.ajax_list_partial = '{}/partials/{}_list_partial.html'.format(self.app,self.model_name)
        return super().dispatch(*args, **kwargs)


class CoreAjaxDetailView(LoginRequiredMixin, AjaxDetailMixin,
                         ModelMixin, DetailView):
    template = ''
    ajax_partial = ''
    model_name = ''
    app = ''
    def dispatch(self, *args, **kwargs):
        self.template = 'detail'
        self.app = self.model._meta.app_label
        self.model_name = self.model.__name__.lower()
        self.ajax_partial = '{}/partials/{}_detail_partial.html'.format(self.app,self.model_name)
        return super().dispatch(*args, **kwargs)



class CoreAjaxUpdateView(LoginRequiredMixin, AjaxUpdateMixin,
                         PassRequestToFormViewMixin,
                         ModelMixin, UpdateView):
    template = ''
    ajax_partial = ''
    ajax_list_partial = ''
    model_name = ''
    app = ''
    def dispatch(self, *args, **kwargs):
        self.template = 'form'
        self.app = self.model._meta.app_label
        self.model_name = self.model.__name__.lower()
        self.ajax_partial = '{}/partials/{}_form_partial.html'.format(self.app,self.model_name)
        self.ajax_list_partial = '{}/partials/{}_list_partial.html'.format(self.app,self.model_name)
        return super().dispatch(*args, **kwargs)

class CoreAjaxDeleteView(LoginRequiredMixin, AjaxDeleteMixin,
                         PassRequestToFormViewMixin,
                         ModelMixin, DeleteView):
    template = ''
    ajax_partial = ''
    ajax_list_partial = ''
    model_name = ''
    app = ''
    def dispatch(self, *args, **kwargs):
        self.template = 'confirm_delete'
        self.app = self.model._meta.app_label
        self.model_name = self.model.__name__.lower()
        self.ajax_partial = '{}/partials/{}_comfirm_delete_partial.html'.format(self.app,self.model_name)
        self.ajax_list_partial = '{}/partials/{}_list_partial.html'.format(self.app,self.model_name)
        return super().dispatch(*args, **kwargs)
