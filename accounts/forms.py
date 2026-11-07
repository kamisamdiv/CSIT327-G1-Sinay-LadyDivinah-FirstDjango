from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import customUser


class BootstrapFormMixin:
    """Adds Bootstrap 5 classes to every field widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css_class = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css_class = "form-select"
            else:
                css_class = "form-control"
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css_class}".strip()


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = customUser
        fields = ("username", "email", "first_name", "last_name", "courses")


class BootstrapAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    pass


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = customUser
        fields = ("first_name", "last_name", "email", "courses")
        labels = {"courses": "Course"}
