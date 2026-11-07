from django.urls import path, include
from django.views.generic import RedirectView
from accounts.admin import admin_site


urlpatterns = [
    path(
        "admin/accounts/login",
        RedirectView.as_view(pattern_name="login", permanent=False),
    ),
    path(
        "admin/accounts/login/",
        RedirectView.as_view(pattern_name="login", permanent=False),
    ),
    path(
        "admin/accounts/signup",
        RedirectView.as_view(pattern_name="signup", permanent=False),
    ),
    path(
        "admin/accounts/signup/",
        RedirectView.as_view(pattern_name="signup", permanent=False),
    ),
    path("admin/", admin_site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("dashboard.urls")),
]