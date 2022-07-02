from django.urls import path


from .views import ProfileDetailView, ProfileUpdateView, ProfileDeleteView


urlpatterns = [
    path('profile/detail/<int:pk>', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/update/<int:pk>', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/delete/<int:pk>', ProfileDeleteView.as_view(), name='profile-delete'),
]
