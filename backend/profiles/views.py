from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.

from addresses.models import Address

from .forms import ProfileForm
from .models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.profile.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['billing_address_list'] = Address.objects.select_related(
            'profile').filter(profile=self.get_object(),
                              address_type=Address.BILLING_ADDRESS)
        context['shipping_address_list'] = Address.objects.select_related(
            'profile').filter(profile=self.get_object(),
                              address_type=Address.SHIPPING_ADDRESS)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.profile.id)

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile-detail',
                            kwargs={'pk': self.get_object().pk})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'profiles/profile_confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.profile.id)

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile-detail',
                            kwargs={'pk': self.get_object().pk})
