from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Profile(models.Model):
    """CyclePrep settings that belong to exactly one user."""

    class CycleType(models.TextChoices):
        REGULAR = "regular", "Regular"
        IRREGULAR = "irregular", "Irregular"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    cycle_type = models.CharField(
        max_length=10,
        choices=CycleType.choices,
        default=CycleType.REGULAR,
    )
    cycle_length = models.PositiveSmallIntegerField(
        "average cycle length (days)",
        default=28,
        validators=[MinValueValidator(15), MaxValueValidator(60)],
        help_text="Days from the start of one period to the start of the next.",
    )
    period_length = models.PositiveSmallIntegerField(
        "average period length (days)",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(14)],
    )
    reminder_days = models.PositiveSmallIntegerField(
        "remind me this many days before",
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        help_text="How early you want a prep reminder before your predicted start.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
