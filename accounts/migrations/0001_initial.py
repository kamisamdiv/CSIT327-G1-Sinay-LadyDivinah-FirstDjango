import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cycle_type",
                    models.CharField(
                        choices=[("regular", "Regular"), ("irregular", "Irregular")],
                        default="regular",
                        max_length=10,
                    ),
                ),
                (
                    "cycle_length",
                    models.PositiveSmallIntegerField(
                        default=28,
                        help_text="Days from the start of one period to the start of the next.",
                        validators=[
                            django.core.validators.MinValueValidator(15),
                            django.core.validators.MaxValueValidator(60),
                        ],
                        verbose_name="average cycle length (days)",
                    ),
                ),
                (
                    "period_length",
                    models.PositiveSmallIntegerField(
                        default=5,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(14),
                        ],
                        verbose_name="average period length (days)",
                    ),
                ),
                (
                    "reminder_days",
                    models.PositiveSmallIntegerField(
                        default=3,
                        help_text="How early you want a prep reminder before your predicted start.",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(7),
                        ],
                        verbose_name="remind me this many days before",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
