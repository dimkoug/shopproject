from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from core.mixins import ModelMixin, PaginationMixin, QueryListMixin, PassRequestToFormViewMixin
from core.functions import is_ajax


class BaseListView(PaginationMixin,QueryListMixin,ModelMixin, LoginRequiredMixin, ListView):
    def get_template_names(self):
        return ['cms/{}/{}_list.html'.format(self.model._meta.app_label,self.model.__name__.lower())]
        
    
    def dispatch(self, *args, **kwargs):
        self.ajax_partial = 'cms/{}/partials/{}_list_partial.html'.format(self.model._meta.app_label,self.model.__name__.lower())
        self.template = self.ajax_partial
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if is_ajax(request):
            html_form = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse(html_form, safe=False)
        return super().get(request, *args, **kwargs)





class BaseDetailView(LoginRequiredMixin,ModelMixin, DetailView):
    def get_template_names(self):
        return ['cms/{}/{}_detail.html'.format(self.model._meta.app_label,self.model.__name__.lower())]


class BaseCreateView(LoginRequiredMixin,ModelMixin, PassRequestToFormViewMixin, CreateView):
    def get_template_names(self):
        return ['cms/{}/{}_form.html'.format(self.model._meta.app_label,self.model.__name__.lower())]

    def get_success_url(self):
        return reverse_lazy('cms:{}-list'.format(self.model.__name__.lower()))

    def form_valid(self, form):
        form.instance._logged_user = self.request.user
        obj = form.save()
        if 'continue' in self.request.POST:
            return redirect(reverse_lazy('cms:{}-update'.format(
                obj.__class__.__name__.lower()),
                kwargs={'pk': obj.pk}))
        if 'new' in self.request.POST:
            return redirect(reverse_lazy('cms:{}-create'.format(
                obj.__class__.__name__.lower())))
        return super().form_valid(obj)

    def form_invalid(self, form, **kwargs):
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return super().form_invalid(form)


class BaseUpdateView(LoginRequiredMixin,ModelMixin, PassRequestToFormViewMixin, UpdateView):
    def get_template_names(self):
        return ['cms/{}/{}_form.html'.format(self.model._meta.app_label,self.model.__name__.lower())]

    def get_success_url(self):
        return reverse_lazy('cms:{}-list'.format(self.model.__name__.lower()))

    def form_valid(self, form):
        form.instance._logged_user = self.request.user
        obj = form.save()
        if 'continue' in self.request.POST:
            return redirect(reverse_lazy('cms:{}-update'.format(
                obj.__class__.__name__.lower()),
                kwargs={'pk': obj.pk}))
        if 'new' in self.request.POST:
            return redirect(reverse_lazy('cms:{}-create'.format(
                obj.__class__.__name__.lower())))
        return super().form_valid(obj)

    def form_invalid(self, form, **kwargs):
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return super().form_invalid(form)


class BaseDeleteView(LoginRequiredMixin,ModelMixin, DeleteView):
    def get_template_names(self):
        return ['cms/{}/{}_confirm_delete.html'.format(self.model._meta.app_label,self.model.__name__.lower())]

    def get_success_url(self):
        return reverse_lazy('cms:{}-list'.format(self.model.__name__.lower()))
    

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Attach the logged-in user to the instance before deleting
        self.object._logged_user = self.request.user
        return super().delete(request, *args, **kwargs)
