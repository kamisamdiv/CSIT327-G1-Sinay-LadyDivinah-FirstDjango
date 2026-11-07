from django.contrib.auth.views import LoginView
from django.urls import path

from .forms import BootstrapAuthenticationForm
from .views import ProfileUpdateView, SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "login/",
        LoginView.as_view(authentication_form=BootstrapAuthenticationForm),
        name="login",
    ),
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
]
