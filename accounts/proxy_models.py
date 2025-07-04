from django.db import models
from django.contrib.auth.models import User

class Coach(User):
    class Meta:
        proxy = True
        verbose_name = "Gestion coach"
        verbose_name_plural = "Gestion coach"

class SuperCoach(User):
    class Meta:
        proxy = True
        verbose_name = "Gestion coach (Admin)"
        verbose_name_plural = "Gestion coach (Admin)"

class Client(User):
    class Meta:
        proxy = True
        verbose_name = "Gestion client"
        verbose_name_plural = "Gestion client"
