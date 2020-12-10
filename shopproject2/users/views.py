from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect

from .forms import UserCreationForm
# Create your views here.

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token


from .models import User
from .forms import AuthenticationForm



def login(request):
    form = AuthenticationForm(request.POST or None)
    if request.method== "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(
                request, 'wrong username or password')
    return render(request, "registration/login.html", {'form':form})


def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            subject = 'Activate Your MySite Account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    return render(request, 'users/signup.html', {'form': form})


class AccountActivationSent(TemplateView):
    template_name = 'users/account_activation_sent.html'


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        auth_login(request, user)
        return redirect('home')
    else:
        return render(request, 'users/account_activation_invalid.html')
