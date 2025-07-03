from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

class AccountsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")
        self.mon_compte_url = reverse("mon compte")

    def test_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_signup_post_valid(self):
        Group.objects.get_or_create(name="client")  # Assure que le groupe existe

        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "SuperPass123!",
            "password2": "SuperPass123!"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/confirmation_sent.html")

        user = User.objects.get(username="testuser")
        self.assertFalse(user.is_active)
        self.assertTrue(user.groups.filter(name="client").exists())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Confirmez votre inscription", mail.outbox[0].subject)

    def test_signup_post_invalid(self):
        response = self.client.post(self.signup_url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_activate_valid_token(self):
        user = User.objects.create_user(
            username="activate_user",
            email="activate@example.com",
            password="testpass123",
            is_active=False
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = reverse("activate", kwargs={"uidb64": uid, "token": token})

        response = self.client.get(url)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertRedirects(response, reverse("dashboard"))

    # def test_activate_invalid_token(self):
    #     user = User.objects.create_user(
    #         username="fake_user",
    #         email="fake@example.com",
    #         password="testpass123",
    #         is_active=False
    #     )
    #     uid = urlsafe_base64_encode(force_bytes(user.pk))
    #     url = reverse("activate", kwargs={"uidb64": uid, "token": "invalid-token"})

    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, "accounts/activation_invalid.html")

    def test_mon_compte_client(self):
        client_user = User.objects.create_user(username="clientuser", password="pass123")
        self.client.login(username="clientuser", password="pass123")
        response = self.client.get(self.mon_compte_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Client")

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")
