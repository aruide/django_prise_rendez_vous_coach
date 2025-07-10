# account/signals.py
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# === ajouter les groupes + permission après le migrate (si groupe pas creer) ===
@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    Group.objects.get_or_create(name='client')
    group_coach, created_coach = Group.objects.get_or_create(name='coach')  
    group_coach_admin, created_coach_admin = Group.objects.get_or_create(name='coach admin')
    
    permissions_seance = Permission.objects.filter(codename__in=[
    'add_seance',
    'change_seance',
    'delete_seance',
    'view_seance',
    ])
    
    
    permissions_coach = Permission.objects.filter(codename__in=[
    'add_client',
    'change_client',
    'delete_client',
    'view_client',
    ])
    
    permissions_coach_admin = Permission.objects.filter(codename__in=[
    'add_coach',
    'change_coach',
    'delete_coach',
    'view_coach',
    ])
    
    group_coach.permissions.set(permissions_coach | permissions_seance)
    group_coach_admin.permissions.set(permissions_coach_admin | permissions_coach | permissions_seance)
    group_coach.save()
    group_coach_admin.save()