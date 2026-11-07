from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.CycleLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileUpdateView.as_view(), name="profile"),
]
