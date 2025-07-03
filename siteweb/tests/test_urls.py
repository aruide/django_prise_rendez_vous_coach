from django.test import TestCase
from django.urls import reverse, resolve
from .. import views

class CoreUrlsTests(TestCase):

    def test_accueil_url_resolves(self):
        url = reverse('accueil')
        self.assertEqual(resolve(url).func, views.accueil)

    def test_info_url_resolves(self):
        url = reverse('info')
        self.assertEqual(resolve(url).func, views.info)

    def test_objectif_url_resolves(self):
        url = reverse('objectif')
        self.assertEqual(resolve(url).func, views.objectif)

    def test_equipe_url_resolves(self):
        url = reverse('equipe')
        self.assertEqual(resolve(url).func, views.equipe)

    def test_accueil_status_code(self):
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)

    def test_info_status_code(self):
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)

    def test_objectif_status_code(self):
        response = self.client.get(reverse('objectif'))
        self.assertEqual(response.status_code, 200)

    def test_equipe_status_code(self):
        response = self.client.get(reverse('equipe'))
        self.assertEqual(response.status_code, 200)
