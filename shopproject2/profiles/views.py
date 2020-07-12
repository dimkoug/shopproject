from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.
from .forms import ProfileForm
from .models import Profile

from core.mixins import ProtectedViewMixin


class ProtectProfile:
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.pk != self.get_object().pk:
            raise PermissionDenied()
        return super().dispatch(*args, **kwargs)


class ProfileDetail(ProtectProfile, ProtectedViewMixin, DetailView):
    model = Profile


class ProfileUpdate(ProtectProfile, ProtectedViewMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile-detail', kwargs = {'pk': self.get_object().pk})
