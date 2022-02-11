from django.urls import path

from rest_framework.authtoken import views

from .views import (
    LoginView, LogoutView, PasswordResetView,
    PasswordResetCompleteView, PasswordResetDoneView,
    PasswordResetConfirmView, AccountActivationSent, activate, SignupView
)


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset', PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('account_activation_sent', AccountActivationSent.as_view(),
         name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('api-token-auth/', views.obtain_auth_token)

]
