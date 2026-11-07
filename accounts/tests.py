from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Profile

User = get_user_model()


class SignUpTests(TestCase):
    def test_signup_creates_user_profile_and_success_message(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "divinah",
                "first_name": "Divinah",
                "email": "divinah@example.com",
                "password1": "Str0ng-Pass-2026",
                "password2": "Str0ng-Pass-2026",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("profile"))
        user = User.objects.get(username="divinah")
        self.assertTrue(Profile.objects.filter(user=user).exists())
        # The success message is rendered on the next page as a Bootstrap alert.
        self.assertContains(response, "alert alert-success")
        self.assertContains(response, "Your account was created successfully")

    def test_signup_page_uses_bootstrap(self):
        response = self.client.get(reverse("signup"))
        self.assertContains(response, "bootstrap@5")
        self.assertContains(response, 'class="form-control"')
        self.assertContains(response, "csrfmiddlewaretoken")


class ProfileAccessTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", "alice@example.com", "Str0ng-Pass-2026")
        self.bob = User.objects.create_user("bob", "bob@example.com", "Str0ng-Pass-2026")

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_user_sees_only_own_profile(self):
        self.client.login(username="alice", password="Str0ng-Pass-2026")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.alice.profile)
        self.assertContains(response, "alice@example.com")
        self.assertNotContains(response, "bob@example.com")

    def test_edit_saves_only_own_profile(self):
        self.client.login(username="alice", password="Str0ng-Pass-2026")
        response = self.client.post(
            reverse("profile"),
            {
                "first_name": "Alice",
                "last_name": "Reyes",
                "email": "alice@example.com",
                "cycle_type": "irregular",
                "cycle_length": 32,
                "period_length": 6,
                "reminder_days": 2,
                # Trying to sneak in another user's id has no effect: the form has no user field.
                "user": self.bob.pk,
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("profile"))
        self.alice.refresh_from_db()
        self.alice.profile.refresh_from_db()
        self.bob.profile.refresh_from_db()
        self.assertEqual(self.alice.first_name, "Alice")
        self.assertEqual(self.alice.profile.cycle_type, "irregular")
        self.assertEqual(self.alice.profile.cycle_length, 32)
        self.assertEqual(self.bob.profile.cycle_length, 28)
        self.assertContains(response, "Your profile was updated.")

    def test_cannot_take_another_users_email(self):
        self.client.login(username="alice", password="Str0ng-Pass-2026")
        response = self.client.post(
            reverse("profile"),
            {
                "email": "bob@example.com",
                "cycle_type": "regular",
                "cycle_length": 28,
                "period_length": 5,
                "reminder_days": 3,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "is-invalid")
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.email, "alice@example.com")

    def test_invalid_cycle_length_is_rejected(self):
        self.client.login(username="alice", password="Str0ng-Pass-2026")
        response = self.client.post(
            reverse("profile"),
            {
                "email": "alice@example.com",
                "cycle_type": "regular",
                "cycle_length": 5,
                "period_length": 5,
                "reminder_days": 3,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.cycle_length, 28)


class LoginTests(TestCase):
    def test_login_page_is_styled_and_works(self):
        User.objects.create_user("carla", "carla@example.com", "Str0ng-Pass-2026")
        page = self.client.get(reverse("login"))
        self.assertContains(page, 'class="form-control"')
        response = self.client.post(
            reverse("login"), {"username": "carla", "password": "Str0ng-Pass-2026"}
        )
        self.assertRedirects(response, reverse("home"))

    def test_logout_is_post_and_redirects_to_login(self):
        User.objects.create_user("dana", "dana@example.com", "Str0ng-Pass-2026")
        self.client.login(username="dana", password="Str0ng-Pass-2026")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
