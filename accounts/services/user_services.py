from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

"""
    Crée un utilisateur inactif à partir d'un formulaire et l'associe à un groupe.

    Args:
        form (forms.ModelForm): Le formulaire contenant les données de l'utilisateur.
        group_name (str, optional): Le nom du groupe auquel l'utilisateur doit être ajouté. 
                                    Par défaut "client".

    Returns:
        User: L'objet utilisateur créé et associé au groupe.
"""
def create_inactive_user_with_group(form, group_name="client"):
    user = form.save(commit=False)
    user.is_active = False
    user.save()

    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    
    return user

"""
    Génère une URL d'activation sécurisée pour un utilisateur donné.

    Args:
        user (User): L'utilisateur pour lequel générer le lien d'activation.
        request (HttpRequest): L'objet request contenant le contexte (utilisé pour le domaine).

    Returns:
        str: L'URL complète d'activation (incluant UID et token).
"""
def generate_activation_url(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    current_site = request.get_host()  # + get_current_site(request).domain possible
    activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    return f"http://{current_site}{activation_link}"

"""
    Active un utilisateur à partir de son identifiant encodé et d’un token de validation.

    Args:
        uidb64 (str): L'identifiant encodé en base64.
        token (str): Le token d'activation généré lors de l'inscription.

    Returns:
        User | None: L'utilisateur activé s'il est valide, sinon None.
"""
def activate_user_from_token(uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return user
    
    return None

"""
    Détermine le rôle d’un utilisateur en fonction de son groupe ou statut superuser.

    Args:
        user (User): L'utilisateur connecté.

    Returns:
        str: "Coach" si l'utilisateur est superuser ou dans un groupe "coach", sinon "Client".
"""
def get_user_role(user):
    if user.is_superuser or user.groups.filter(name__in=["coach", "coach admin"]).exists():
        return "Coach"
    return "Client"