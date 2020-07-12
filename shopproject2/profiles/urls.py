from django.urls import path


from .views import ProfileDetail, ProfileUpdate


urlpatterns = [
    path('profile-detail/<int:pk>', ProfileDetail.as_view(), name='profile-detail'),
    path('profile-update/<int:pk>', ProfileUpdate.as_view(), name='profile-update'),
]
