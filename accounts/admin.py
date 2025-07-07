from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .proxy_models import Coach, SuperCoach, Client
from .forms import CustomUserChangeForm

User = get_user_model()

admin.site.site_header = "⛵ Admin de CoachéCoulé"
admin.site.site_title = "Admin - CoachéCoulé"
admin.site.index_title = "Tableau de bord pirate"

liste_fieldsets = (
            (None, {'fields': ('username', 'password')}),
            ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'photo')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
        )

liste_add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'photo', 'password1', 'password2'),
        }),
    )

# === Admin pour Coach ===
class CoachAdmin(BaseUserAdmin):
    form = CustomUserChangeForm

    fieldsets = liste_fieldsets

    add_fieldsets = liste_add_fieldsets
    
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
    form = CustomUserChangeForm

    fieldsets = liste_fieldsets

    add_fieldsets = liste_add_fieldsets
    
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
    form = CustomUserChangeForm

    fieldsets = liste_fieldsets

    add_fieldsets = liste_add_fieldsets
    
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

