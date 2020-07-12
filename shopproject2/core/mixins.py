from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages


class ProtectedViewMixin:

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect(reverse_lazy('login') + '?next={}'.format(self.request.path))
        return super().dispatch(*args, **kwargs)


class ModelMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        return context


class UUidMixinQuery:
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = super().get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(uuid=pk)
        obj = queryset.get()
        return obj


class SuccessUrlMixin:
    def get_success_url(self):
        model_name = self.model.__name__.lower()
        app = self.model._meta.app_label
        return reverse_lazy("{}:{}-list".format(app, model_name))


class MessageMixin:
    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, 'Your {} was proccesed successfully!'.format(
                self.model.__name__))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'error ocured for {}'.format(
                self.model.__name__))
        return super().form_invalid(form)


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
