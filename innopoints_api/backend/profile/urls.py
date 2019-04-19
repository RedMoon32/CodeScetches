from django.urls import path

from profile.views import LoginView, ProfileView

urlpatterns = [
    path("userinfo/", ProfileView.as_view(), name='userinfo')
]
