from django.urls import path, include

from rest_framework.authtoken import views

from .views import (
    UserLoginView, UserLogoutView, UserPasswordResetView,
    UserPasswordResetCompleteView, UserPasswordResetDoneView,
    UserPasswordResetConfirmView, AccountActivationSent, activate, SignupView
)


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password_reset', UserPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done', UserPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/',
         UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done', UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('account_activation_sent', AccountActivationSent.as_view(),
         name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/',include('users.users_api.routers')),

]
