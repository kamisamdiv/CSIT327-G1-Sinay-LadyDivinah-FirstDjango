from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "cycle_type", "cycle_length", "period_length", "reminder_days", "updated_at")
    list_filter = ("cycle_type",)
    search_fields = ("user__username", "user__email")
