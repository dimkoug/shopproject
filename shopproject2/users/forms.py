from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm


class UserCreationForm(BaseUserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'birth_date', 'password1', 'password2', )
