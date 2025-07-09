from django.test import TestCase
from django.utils import timezone
from datetime import datetime, time, timedelta, date
from rdv.forms import SeanceForm, AnnulationForm
from rdv.models import Seance
from django.contrib.auth import get_user_model

User = get_user_model()

class SeanceFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')

    def test_form_valid_data(self):
        # Créneau valide dans le futur et heure valide
        form_data = {
            'date': (timezone.now().date() + timedelta(days=1)).isoformat(),
            'heure_debut': '09:00',
            'objet': 'Test rendez-vous',
        }
        form = SeanceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_date_in_past(self):
        form_data = {
            'date': (timezone.now().date() - timedelta(days=1)).isoformat(),
            'heure_debut': '09:00',
            'objet': 'Test',
        }
        form = SeanceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("La date ne peut pas être dans le passé.", form.errors['__all__'])

    def test_form_heure_en_dehors_des_heures_autorisees(self):
        form_data = {
            'date': (timezone.now().date() + timedelta(days=1)).isoformat(),
            'heure_debut': '07:59',
            'objet': 'Test',
        }
        form = SeanceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Les rendez-vous doivent être entre 08h00 et 20h00.", form.errors['__all__'])

        form_data['heure_debut'] = '20:00'
        form = SeanceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Les rendez-vous doivent être entre 08h00 et 20h00.", form.errors['__all__'])

    def test_form_creneau_deja_reserve(self):
        # On crée une séance pour bloquer un créneau
        Seance.objects.create(
            client=self.user,
            date=timezone.now().date() + timedelta(days=1),
            heure_debut=time(10, 0),
            objet='Existing',
        )
        form_data = {
            'date': (timezone.now().date() + timedelta(days=1)).isoformat(),
            'heure_debut': '10:00',
            'objet': 'Test',
        }
        form = SeanceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Ce créneau est déjà réservé.", form.errors['__all__'])

    def test_form_creneau_trop_proche(self):
        # Séance existante à 10:00
        Seance.objects.create(
            client=self.user,
            date=timezone.now().date() + timedelta(days=1),
            heure_debut=time(10, 0),
            objet='Existing',
        )
        # Essayer à 10:05 => trop proche (moins de 10 minutes)
        form_data = {
            'date': (timezone.now().date() + timedelta(days=1)).isoformat(),
            'heure_debut': '10:05',
            'objet': 'Test',
        }
        form = SeanceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Un autre rendez-vous est trop proche (10 min).", form.errors['__all__'])


class AnnulationFormTests(TestCase):
    def test_motif_annulation_valide(self):
        seance = Seance.objects.create(
            client=User.objects.create_user('user2'),
            date=timezone.now().date() + timedelta(days=1),
            heure_debut=time(12, 0),
            objet='Test',
        )
        form_data = {'motif_annulation': 'Je suis malade'}
        form = AnnulationForm(data=form_data, instance=seance)
        self.assertTrue(form.is_valid())

    def test_motif_annulation_vide(self):
        seance = Seance.objects.create(
            client=User.objects.create_user('user3'),
            date=timezone.now().date() + timedelta(days=1),
            heure_debut=time(14, 0),
            objet='Test',
        )
        form_data = {'motif_annulation': ''}
        form = AnnulationForm(data=form_data, instance=seance)
        self.assertFalse(form.is_valid())
        self.assertIn("Vous devez saisir un motif d'annulation.", form.errors['motif_annulation'])
