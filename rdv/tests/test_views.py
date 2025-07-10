from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.timezone import now, timedelta
from rdv.models import Seance

User = get_user_model()

class RdvViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Création des groupes
        self.client_group, _ = Group.objects.get_or_create(name='client')
        self.coach_group, _ = Group.objects.get_or_create(name='coach')

        # Utilisateurs
        self.client_user = User.objects.create_user(username='clientuser', password='pass123')
        self.client_user.groups.add(self.client_group)

        self.coach_user = User.objects.create_user(username='coachuser', password='pass123')
        self.coach_user.groups.add(self.coach_group)

        # Séance à venir et passée
        self.seance_avenir = Seance.objects.create(
            client=self.client_user,
            date=(now() + timedelta(days=1)).date(),
            heure_debut=(now() + timedelta(hours=1)).time(),
            statut="valide"
        )

        self.seance_passee = Seance.objects.create(
            client=self.client_user,
            date=(now() - timedelta(days=1)).date(),
            heure_debut=(now() - timedelta(hours=1)).time(),
            statut="valide"
        )

    def test_dashboard_client(self):
        self.client.login(username='clientuser', password='pass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdv/dashboard_client.html')
        self.assertIn(self.seance_avenir, response.context['seances_avenir'])
        self.assertIn(self.seance_passee, response.context['seances_passees'])

    def test_dashboard_coach(self):
        self.client.login(username='coachuser', password='pass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdv/dashboard_coach.html')
        self.assertContains(response, "Coach")  # Optionnel, selon le contenu de ton template

    def test_prendre_rdv_get(self):
        self.client.login(username='clientuser', password='pass123')
        response = self.client.get(reverse('prendre_rdv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdv/prise_rdv.html')

    # def test_prendre_rdv_post_valid(self):
    #     self.client.login(username='clientuser', password='pass123')
    #     response = self.client.post(reverse('prendre_rdv'), {
    #         "date": (now() + timedelta(days=2)).date(),
    #         "heure_debut": "10:00",
    #         "heure_fin": "11:00",
    #         "statut": "valide"
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, reverse('dashboard'))
    #     self.assertEqual(Seance.objects.filter(client=self.client_user).count(), 3)

    def test_seance_detail_access_by_client_owner(self):
        self.client.login(username='clientuser', password='pass123')
        url = reverse('seance_detail', args=[self.seance_avenir.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdv/seance_detail.html')

    # def test_seance_detail_access_denied_to_other_client(self):
    #     other_client = User.objects.create_user(username='otherclient', password='pass123')
    #     other_client.groups.add(self.client_group)
    #     self.client.login(username='otherclient', password='pass123')
    #     url = reverse('seance_detail', args=[self.seance_avenir.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 403)

    def test_annuler_seance_get(self):
        self.client.login(username='clientuser', password='pass123')
        url = reverse('annuler_seance', args=[self.seance_avenir.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rdv/annule_seance.html')

    def test_annuler_seance_post(self):
        self.client.login(username='clientuser', password='pass123')
        url = reverse('annuler_seance', args=[self.seance_avenir.id])
        response = self.client.post(url, {
            "motif_annulation": "Empêchement",
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.seance_avenir.refresh_from_db()
        self.assertEqual(self.seance_avenir.statut, 'annule')
