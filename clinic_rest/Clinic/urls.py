from django.contrib import admin
from django.urls import path, include
from backend.Clinic.Profile_Views import LoginView, ProfileView, RegView, ChangePasswordView
from backend.Clinic.Clinic_Views import ApointmentView, DoctorsView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('register/', RegView.as_view()),
    path('doctors/', DoctorsView.as_view()),
    path('appointments/', ApointmentView.as_view()),
    path('password/', ChangePasswordView.as_view())

]
