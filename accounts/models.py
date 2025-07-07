from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.nom} {self.prenom})"