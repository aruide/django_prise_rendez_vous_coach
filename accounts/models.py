from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    description_personnelle = models.TextField(verbose_name="Description personelle", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.photo and not self._state.adding:
            # si déjà une image et modification, ne pas la renommer de nouveau
            return super().save(*args, **kwargs)

        if self.photo:
            ext = os.path.splitext(self.photo.name)[1]
            nouveau_nom = f"{slugify(self.username)}-avatar{ext}"
            self.photo.name = f"photos/{nouveau_nom}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.nom} {self.prenom})"