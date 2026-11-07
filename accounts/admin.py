from functools import wraps

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from .models import customUser


class RoleBasedAdminSite(admin.AdminSite):
  def has_permission(self, request):
    user = request.user
    return (
        user.is_active
        and (
            user.is_superuser
            or (
                user.is_staff
                and user.role == customUser.Role.ADMIN
            )
        )
    )

  def admin_view(self, view, cacheable=False):
    admin_view = super().admin_view(view, cacheable)

    @wraps(view)
    def role_checked_view(request, *args, **kwargs):
      if request.user.is_authenticated and not self.has_permission(request):
        raise PermissionDenied
      return admin_view(request, *args, **kwargs)

    return role_checked_view


admin_site = RoleBasedAdminSite(name="admin")


@admin.register(customUser, site=admin_site)
class customUserAdmin(UserAdmin):
  list_display = [
      'first_name',
      'last_name',
      'username',
      'email',
      'role',
      'is_staff',
  ]

  fieldsets = UserAdmin.fieldsets + (
      ("School Profile", {"fields": ("role", "courses")}),  # Updated to 'courses'
  )