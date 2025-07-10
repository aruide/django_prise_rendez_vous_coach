# rdv/services/seance_services.py

from django.utils.timezone import make_aware
from datetime import datetime, date, time
from ..models import Seance

"""
    Vérifie si l'utilisateur est un coach, un coach admin ou un superutilisateur.

    Args:
        user (User): L'utilisateur à vérifier.

    Returns:
        bool: True si l'utilisateur est coach/admin/superuser, sinon False.
"""
def is_user_coach(user):
    return user.groups.filter(name__in=['coach', 'coach admin']).exists() or user.is_superuser

"""
    Récupère les séances accessibles pour l'utilisateur donné.

    - Si l'utilisateur est un coach/admin/superuser : toutes les séances sont retournées.
    - Si c'est un client : seules ses propres séances sont retournées.

    Args:
        user (User): L'utilisateur connecté.

    Returns:
        QuerySet: Les séances triées par date et heure.
"""
def get_user_seances(user):
    if is_user_coach(user):
        return Seance.objects.all().order_by('date', 'heure_debut')
    else:
        return Seance.objects.filter(client=user).order_by('date', 'heure_debut')

"""
    Sépare les séances en deux listes : à venir et passées.

    Args:
        seances (Iterable[Seance]): Une liste ou un QuerySet de séances.

    Returns:
        tuple: Un tuple contenant deux listes :
            - seances_avenir (list)
            - seances_passees (list)
"""
def split_seances_future_past(seances):
    now = make_aware(datetime.now())
    seances_avenir = [s for s in seances if make_aware(datetime.combine(s.date, s.heure_debut)) >= now]
    seances_passees = [s for s in seances if make_aware(datetime.combine(s.date, s.heure_debut)) < now]
    return seances_avenir, seances_passees

"""
    Vérifie si l'utilisateur a le droit de voir une séance spécifique.

    - Les clients ne peuvent voir que leurs propres séances.
    - Les coachs/admins peuvent tout voir.

    Args:
        user (User): L'utilisateur connecté.
        seance (Seance): La séance à vérifier.

    Returns:
        bool: True si l'utilisateur peut voir la séance, sinon False.
"""
def user_can_view_seance(user, seance):
    return not user.groups.filter(name='client').exists() or seance.client == user

"""
    Met à jour la note du coach associée à une séance.

    Args:
        seance (Seance): La séance à mettre à jour.
        note (str): Le texte de la note.

    Returns:
        None
"""
def update_note_coach(seance, note):
    seance.note_coach = note
    seance.save()

"""
    Annule une séance en modifiant son statut à 'annule'.

    Args:
        seance (Seance): La séance à annuler.

    Returns:
        None
"""
def annuler_seance_instance(seance):
    seance.statut = 'annule'
    seance.save()