from django import forms
from .models import Profile


from core.forms import BootstrapForm

class ProfileForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)
