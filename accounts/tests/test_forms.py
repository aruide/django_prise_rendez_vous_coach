from django.test import TestCase
from accounts.forms import CustomSignupForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSignupFormTests(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'nouvel_utilisateur',
            'email': 'user@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        form = CustomSignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_if_username_taken(self):
        # Créer un utilisateur avec ce username
        User.objects.create_user(username='existant', email='e@mail.com', password='Pass1234')

        form_data = {
            'username': 'existant',  # username déjà pris
            'email': 'user2@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'], ["Ce nom d'utilisateur est déjà utilisé."])

    def test_invalid_if_passwords_do_not_match(self):
        form_data = {
            'username': 'utilisateur2',
            'email': 'user2@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'MismatchPass!',
        }
        form = CustomSignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
