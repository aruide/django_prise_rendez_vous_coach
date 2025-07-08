# accounts/views.py
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .forms import CustomSignupForm
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from core.decorators import logout_required

from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views
from django.urls import path

User = get_user_model()

@logout_required
def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Compte inactif jusqu'à activation par email
            user.save()

            # Ajouter au groupe "client"
            group, _ = Group.objects.get_or_create(name="client")
            user.groups.add(group)

            # Générer le lien d’activation
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            activation_url = f"http://{current_site.domain}{activation_link}"

            print("🔗 Lien d’activation :", activation_url)  # Pour debug

            # Préparer l'email
            subject = "Confirmez votre inscription"
            from_email = 'noreply@monsite.fr'
            to_email = [user.email]

            text_content = f"Bonjour {user.username}, cliquez ici pour activer votre compte : {activation_url}"

            html_content = render_to_string("accounts/activation_email.html", {
                'user': user,
                'activation_url': activation_url
            })

            # Envoi de l'email avec gestion des erreurs
            try:
                email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                email.attach_alternative(html_content, "text/html")
                email.send()
                print("✅ Email envoyé à", user.email)
            except Exception as e:
                print("❌ Erreur lors de l'envoi de l'email :", e)

            return render(request, 'accounts/confirmation_sent.html')

    else:
        form = CustomSignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("dashboard")  # ou une page de confirmation
    else:
        return render(request, "accounts/activation_invalid.html")

@login_required
def mon_compte(request):
    user = request.user
    
    if user.groups.filter(name__in=["coach", "coach admin"]).exists() or user.is_superuser:
        role = "Coach"
    else:
        role = "Client"
    
    return render(request, 'accounts/mon_compte.html', {
        'user': user,
        'role': role
    })
    
@method_decorator(logout_required, name='dispatch')
class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'