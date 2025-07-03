from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class CustomUserModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="johndoe",
            password="testpass123",
            prenom="John",
            nom="Doe"
        )

    def test_user_str_method(self):
        self.assertEqual(str(self.user), "johndoe (Doe John)")

    def test_create_user_with_photo_renamed(self):
        # Création d'une fausse image
        image = SimpleUploadedFile(
            name="profile.jpg",
            content=b"fake image content",
            content_type="image/jpeg"
        )

        user = User.objects.create_user(
            username="janedoe",
            password="securepass",
            prenom="Jane",
            nom="Doe",
            photo=image
        )

        # Vérifie que le nom du fichier a bien été modifié selon le slug
        self.assertTrue(user.photo.name.startswith("photos/janedoe-avatar"))
        self.assertTrue(user.photo.name.endswith(".jpg"))