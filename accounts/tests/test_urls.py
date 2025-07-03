from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

class AccountsURLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.user.is_active = False
        self.user.save()

    def test_signup_url(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('logout'))
        self.assertIn(response.status_code, [302, 200])  # souvent redirection

    def test_mon_compte_authenticated(self):
        self.user.is_active = True
        self.user.save()
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('mon compte'))
        self.assertEqual(response.status_code, 200)

    def test_mon_compte_unauthenticated(self):
        response = self.client.get(reverse('mon compte'))
        self.assertEqual(response.status_code, 302)  # Redirection vers login

    def test_activate_valid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirection vers dashboard ou autre

    # def test_activate_invalid_token(self):
    #     uid = urlsafe_base64_encode(force_bytes(self.user.pk))
    #     token = 'invalid-token'
    #     url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, 'accounts/activation_invalid.html')
    #     self.assertEqual(response.status_code, 200)
