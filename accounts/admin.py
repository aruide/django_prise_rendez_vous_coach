from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .proxy_models import Coach, SuperCoach, Client

User = get_user_model()

# === Admin pour Coach ===
class CoachAdmin(BaseUserAdmin):
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        obj.is_staff = True  # coach n'est pas staff
        super().save_model(request, obj, form, change)

        if is_new:
            # On attribue seulement le groupe 'coach'
            try:
                group = Group.objects.get(name='coach')
                obj.groups.set([group])  # Remplace tous les groupes par 'coach'
            except Group.DoesNotExist:
                pass

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {'title': 'Ajouter un coach'}
        return super().add_view(request, form_url, extra_context=extra_context)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            coach_group = Group.objects.get(name="coach")
            return qs.filter(groups=coach_group)
        except Group.DoesNotExist:
            return qs

# === Admin pour SuperCoach ===
class SuperCoachAdmin(BaseUserAdmin):
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        obj.is_staff = True  # supercoach est staff
        super().save_model(request, obj, form, change)

        if is_new:
            try:
                group = Group.objects.get(name='coach admin')
                obj.groups.set([group])  # Remplace tous les groupes par 'coach_admin'
            except Group.DoesNotExist:
                pass

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {'title': 'Ajouter un coach (Admin)'}
        return super().add_view(request, form_url, extra_context=extra_context)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            coach_group = Group.objects.get(name="coach admin")
            return qs.filter(groups=coach_group, is_staff=True)
        except Group.DoesNotExist:
            return qs
        
class ClientAdmin(BaseUserAdmin):
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        obj.is_staff = False  # client n'est pas staff
        super().save_model(request, obj, form, change)

        if is_new:
            # On attribue seulement le groupe 'coach'
            try:
                group = Group.objects.get(name='client')
                obj.groups.set([group])  # Remplace tous les groupes par 'coach'
            except Group.DoesNotExist:
                pass

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {'title': 'Ajouter un client'}
        return super().add_view(request, form_url, extra_context=extra_context)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            coach_group = Group.objects.get(name="client")
            return qs.filter(groups=coach_group)
        except Group.DoesNotExist:
            return qs


# === Enregistrement des modèles proxy ===
admin.site.register(Coach, CoachAdmin)
admin.site.register(SuperCoach, SuperCoachAdmin)
admin.site.register(Client, ClientAdmin)

