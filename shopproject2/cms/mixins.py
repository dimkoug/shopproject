from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.conf import settings

class SuccessUrlMixin:
    def get_success_url(self):
        model_name = self.model.__name__.lower()
        app = self.model._meta.app_label
        return reverse_lazy("cms:{}-list".format(model_name))

class DynamicTemplateMixin:

    def get_template_names(self):
        model_name = self.model.__name__.lower()
        view_template = ""
        app = self.model._meta.app_label
        template = self.template
        if template == 'list':
            view_template =  "cms/{}/{}_list.html".format(app,model_name)
        if template == 'detail':
            view_template =  "cms/{}/{}_detail.html".format(app,model_name)
        if template == 'form':
            view_template =  "cms/{}/{}_form.html".format(app,model_name)
        if template == 'delete':
            view_template =  "cms/{}/{}_confirm_delete.html".format(app,model_name)
        return [view_template]


class MessageMixin:
    def form_valid(self, form):
        obj = form.save()
        model_name = self.model.__name__.lower()
        if 'new' in self.request.POST:
            return redirect(reverse_lazy("cms:{}-create".format(model_name)))
        if 'continue' in self.request.POST:
            return redirect(reverse_lazy("cms:{}-update".format(model_name), kwargs={"pk":obj.pk}))
        messages.success(
            self.request, 'Your {} was proccesed successfully!'.format(
                self.model.__name__))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'error ocured for {}'.format(
                self.model.__name__))
        return super().form_invalid(form)
