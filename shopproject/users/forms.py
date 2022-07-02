from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    AuthenticationForm as BaseAuthenticationForm,
    PasswordResetForm as BasePasswordResetForm,
    UserCreationForm as BaseUserCreationForm,
    SetPasswordForm as BaseSetPasswordForm,
)

from core.forms import BootstrapForm

User = get_user_model()


class UserCreationForm(BootstrapForm, BaseUserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'birth_date', 'password1', 'password2', )


class UserAuthenticationForm(BootstrapForm, BaseAuthenticationForm):
    pass


class UserPasswordResetForm(BootstrapForm, BasePasswordResetForm):
    pass


class UserSetPasswordForm(BootstrapForm, BaseSetPasswordForm):
    pass
