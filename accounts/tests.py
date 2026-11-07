from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class SignUpTests(TestCase):
    def test_signup_shows_success_message(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newstudent",
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "Student",
                "courses": "BSIT",
                "password1": "Str0ng-Passw0rd!",
                "password2": "Str0ng-Passw0rd!",
            },
            follow=True,
        )
        self.assertTrue(User.objects.filter(username="newstudent").exists())
        self.assertRedirects(response, reverse("login"))
        self.assertContains(response, "alert-success")
        self.assertContains(response, "Account created for newstudent")


class ProfileTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(
            username="alice", password="Str0ng-Passw0rd!", first_name="Alice"
        )
        self.bob = User.objects.create_user(
            username="bob", password="Str0ng-Passw0rd!", first_name="Bob"
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('profile')}"
        )

    def test_profile_shows_logged_in_user(self):
        self.client.login(username="alice", password="Str0ng-Passw0rd!")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.alice)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_user_can_update_own_profile(self):
        self.client.login(username="alice", password="Str0ng-Passw0rd!")
        response = self.client.post(
            reverse("profile"),
            {
                "first_name": "Alicia",
                "last_name": "Reyes",
                "email": "alicia@example.com",
                "courses": "BSCS",
            },
            follow=True,
        )
        self.alice.refresh_from_db()
        self.assertEqual(self.alice.first_name, "Alicia")
        self.assertEqual(self.alice.courses, "BSCS")
        self.assertContains(response, "Your profile was updated.")

    def test_user_cannot_edit_another_users_profile(self):
        self.client.login(username="alice", password="Str0ng-Passw0rd!")
        # Even if someone tries to pass another user's id, the view
        # always edits request.user.
        self.client.post(
            reverse("profile") + f"?pk={self.bob.pk}",
            {"first_name": "Hacked", "last_name": "", "email": "", "courses": ""},
        )
        self.bob.refresh_from_db()
        self.assertEqual(self.bob.first_name, "Bob")

    def test_pages_use_bootstrap(self):
        for name in ("login", "signup"):
            response = self.client.get(reverse(name))
            self.assertContains(response, "bootstrap@5")
            self.assertContains(response, 'class="form-control"')
