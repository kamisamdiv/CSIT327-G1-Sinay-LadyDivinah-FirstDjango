from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    STUDENT = "STUDENT", "Student"
    ADMIN = "ADMIN", "Administrator"


class customUser(AbstractUser):
    Role = Role
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    courses = models.CharField(max_length=100, blank=True, null=True)


CustomUser = customUser