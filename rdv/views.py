from core.decorators import route

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SeanceForm
from .models import Seance

def accueil(request):
    return render(request, "rdv/accueil.html")

@login_required
def dashboard(request):
    if request.user.groups.filter(name='coach').exists() or request.user.is_superuser:
        seances = Seance.objects.all().order_by('date', 'heure_debut')
        return render(request, 'rdv/dashboard_coach.html', {'seances': seances})
    else:
        seances = Seance.objects.filter(client=request.user).order_by('date', 'heure_debut')
        return render(request, 'rdv/dashboard_client.html', {'seances': seances})    

@login_required
def prendre_rdv(request):
    if request.method == "POST":
        form = SeanceForm(request.POST)
        if form.is_valid():
            seance = form.save(commit=False)
            seance.client = request.user
            seance.save()
            return redirect('dashboard')
    else:
        form = SeanceForm()
    return render(request, 'prise_rdv.html', {'form': form})