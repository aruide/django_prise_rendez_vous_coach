from django.db import models
from django.conf import settings

class Seance(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    heure_debut = models.TimeField()
    objet = models.CharField(max_length=200)
    note_coach = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.client.username

    class Meta:
        unique_together = ('date', 'heure_debut')  # Évite les conflits