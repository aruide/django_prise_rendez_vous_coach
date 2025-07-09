from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Seance(models.Model):
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('annule', 'Annulé'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    heure_debut = models.TimeField()
    objet = models.CharField(max_length=200)
    note_coach = models.TextField(blank=True, null=True)

    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='actif'
    )

    motif_annulation = models.TextField(
        blank=True,
        null=True,
        help_text="Motif de l'annulation (à remplir si statut = annulé)"
    )
    
    def clean(self):
        if self.statut == 'annule' and not self.motif_annulation:
            raise ValidationError("Le motif d'annulation est obligatoire si la séance est annulée.")

    def __str__(self):
        return f"{self.client.username} - {self.date} {self.heure_debut} ({self.statut})"

    class Meta:
        unique_together = ('date', 'heure_debut')
