# accounts/views.py
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomSignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from core.decorators import logout_required

from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views

from .services.user_services import create_inactive_user_with_group, generate_activation_url, activate_user_from_token, get_user_role
from .services.email_services import send_activation_email


User = get_user_model()

@logout_required
def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = create_inactive_user_with_group(form)
            activation_url = generate_activation_url(user, request)

            try:
                send_activation_email(user, activation_url)
                print("Email envoyé à", user.email)
            except Exception as e:
                print("Erreur lors de l'envoi de l'email :", e)

            return render(request, 'accounts/confirmation_sent.html')
    else:
        form = CustomSignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def activate(request, uidb64, token):
    user = activate_user_from_token(uidb64, token)

    if user:
        login(request, user)
        return redirect("dashboard")
    else:
        return render(request, "accounts/activation_invalid.html")
    
    
@login_required
def mon_compte(request):
        
    return render(request, 'accounts/mon_compte.html', {
        'user': request.user,
        'role': get_user_role(request.user)
    })
        
@method_decorator(logout_required, name='dispatch')
class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'