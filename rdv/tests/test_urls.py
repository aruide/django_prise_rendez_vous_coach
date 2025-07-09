from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from rdv import views

User = get_user_model()

class UrlsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.client.login(username='testuser', password='pass123')

    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, views.dashboard)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_prendre_rdv_url_resolves(self):
        url = reverse('prendre_rdv')
        self.assertEqual(resolve(url).func, views.prendre_rdv)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_seance_detail_url_resolves(self):
        # Création d'une séance pour test
        from rdv.models import Seance
        seance = Seance.objects.create(
            client=self.user,
            date='2099-12-31',
            heure_debut='10:00',
            objet='Test'
        )
        url = reverse('seance_detail', args=[seance.id])
        self.assertEqual(resolve(url).func, views.seance_detail)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_annuler_seance_url_resolves(self):
        from rdv.models import Seance
        seance = Seance.objects.create(
            client=self.user,
            date='2099-12-31',
            heure_debut='10:00',
            objet='Test'
        )
        url = reverse('annuler_seance', args=[seance.id])
        self.assertEqual(resolve(url).func, views.annuler_seance)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
