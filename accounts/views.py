from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import LoginForm, ProfileForm, SignUpForm
from .models import Profile


class HomeView(TemplateView):
    template_name = "home.html"


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("profile")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)  # saves the user as self.object
        login(self.request, self.object)
        messages.success(
            self.request,
            f"Welcome to CyclePrep, {self.object.username}! Your account was created successfully. "
            "Take a moment to set up your cycle settings below.",
        )
        return response


class CycleLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View and edit the logged-in user's own profile.

    The URL has no pk or username: get_object() always returns the profile of
    request.user, so there is no way to open or edit someone else's profile.
    LoginRequiredMixin sends anonymous visitors to the login page.
    """

    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("profile")
    success_message = "Your profile was updated."

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile
