from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class SitewebViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()

        # Création d'un coach
        self.coach_group, _ = Group.objects.get_or_create(name='coach')
        self.user_coach = self.user_model.objects.create_user(username="coach1", password="test1234")
        self.user_coach.groups.add(self.coach_group)

        # Création d'un client
        self.user = self.user_model.objects.create_user(username="client", password="test1234")

    def test_accueil_view(self):
        response = self.client.get(reverse("accueil"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "siteweb/accueil.html")

    def test_info_view(self):
        response = self.client.get(reverse("info"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "siteweb/info.html")

    def test_objectif_view(self):
        response = self.client.get(reverse("objectif"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "siteweb/objectif.html")

    def test_equipe_view(self):
        response = self.client.get(reverse("equipe"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "siteweb/equipe.html")
        # Vérifie que le coach est dans le contexte
        self.assertIn(self.user_coach, response.context["coachs"])
        # Vérifie que le client normal n'est pas dans le contexte
        self.assertNotIn(self.user, response.context["coachs"])
