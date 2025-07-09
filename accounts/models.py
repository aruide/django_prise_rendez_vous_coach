from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from slugify import slugify

class CustomUser(AbstractUser):
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    description_personnelle = models.TextField(verbose_name="Description personelle", blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            old_user = CustomUser.objects.get(pk=self.pk)
            old_photo = old_user.photo
        except CustomUser.DoesNotExist:
            old_photo = None

        # Si une nouvelle photo est fournie (upload)
        if self.photo and (not old_photo or self.photo.name != old_photo.name):
            ext = os.path.splitext(self.photo.name)[1]
            nouveau_nom = f"{slugify(self.username)}-avatar{ext}"
            self.photo.name = f"{nouveau_nom}"

            # Supprimer l'ancienne si le nom est différent
            if old_photo and old_photo.name != self.photo.name:
                old_photo.delete(save=False)

        # Si l’utilisateur a supprimé l’image volontairement (photo = None)
        if not self.photo and old_photo and 'photo' in self.__dict__:
            old_photo.delete(save=False)

        super().save(*args, **kwargs)    
    
    def delete(self, *args, **kwargs):
        if self.photo:
            self.photo.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.nom} {self.prenom})"