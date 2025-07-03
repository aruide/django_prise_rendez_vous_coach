from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date, time

from ..models import Seance

User = get_user_model()

class SeanceModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_creation_seance_simple(self):
        seance = Seance.objects.create(
            client=self.user,
            date=date(2025, 7, 9),
            heure_debut=time(14, 0),
            objet="Coaching Python"
        )
        self.assertEqual(seance.client, self.user)
        self.assertEqual(seance.statut, 'actif')  # statut par défaut
        self.assertEqual(str(seance), f"{self.user.username} - 2025-07-09 14:00:00 (actif)")

    def test_validation_annulation_sans_motif(self):
        seance = Seance(
            client=self.user,
            date=date(2025, 7, 9),
            heure_debut=time(15, 0),
            objet="Coaching Django",
            statut='annule',
            motif_annulation=None
        )
        with self.assertRaises(ValidationError) as context:
            seance.clean()
        self.assertIn("Le motif d'annulation est obligatoire", str(context.exception))

    def test_validation_annulation_avec_motif(self):
        seance = Seance(
            client=self.user,
            date=date(2025, 7, 9),
            heure_debut=time(16, 0),
            objet="Coaching Django",
            statut='annule',
            motif_annulation="Client indisponible"
        )
        # Ne doit pas lever d'erreur
        try:
            seance.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

    def test_unique_date_heuredebut(self):
        Seance.objects.create(
            client=self.user,
            date=date(2025, 7, 10),
            heure_debut=time(10, 0),
            objet="Séance 1"
        )
        seance2 = Seance(
            client=self.user,
            date=date(2025, 7, 10),
            heure_debut=time(10, 0),
            objet="Séance 2"
        )
        with self.assertRaises(Exception):
            seance2.save()

