from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SeanceForm
from .models import Seance

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Seance
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

@login_required
def dashboard(request):
    now = make_aware(datetime.now())

    is_coach = request.user.groups.filter(name__in=['coach', 'coach admin']).exists() or request.user.is_superuser

    if is_coach:
        seances = Seance.objects.all().order_by('date', 'heure_debut')
    else:
        seances = Seance.objects.filter(client=request.user).order_by('date', 'heure_debut')

    # Séparer à venir et passées
    seances_avenir = [s for s in seances if make_aware(datetime.combine(s.date, s.heure_debut)) >= now]
    seances_passees = [s for s in seances if make_aware(datetime.combine(s.date, s.heure_debut)) < now]

    # Pagination
    page_avenir = request.GET.get('page_avenir')
    page_passees = request.GET.get('page_passees')

    paginator_avenir = Paginator(seances_avenir, 5)
    paginator_passees = Paginator(seances_passees, 5)

    seances_avenir_page = paginator_avenir.get_page(page_avenir)
    seances_passees_page = paginator_passees.get_page(page_passees)

    context = {
        'seances_avenir': seances_avenir_page,
        'seances_passees': seances_passees_page,
        'user': request.user,
    }

    if is_coach:
        return render(request, 'rdv/dashboard_coach.html', context)
    else:
        return render(request, 'rdv/dashboard_client.html', context)
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
    return render(request, 'rdv/prise_rdv.html', {'form': form})

@login_required
def seance_detail(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)

    # Permissions : un client ne peut voir que ses séances
    if request.user.groups.filter(name='client').exists() and seance.client != request.user:
        return render(request, '403.html', status=403)

    is_coach = request.user.groups.filter(name__in=['coach', 'coach admin']).exists() or request.user.is_superuser

    if request.method == 'POST' and is_coach:
        new_note = request.POST.get('note_coach')
        seance.note_coach = new_note
        seance.save()
        return redirect('seance_detail', seance_id=seance.id)

    return render(request, 'rdv/seance_detail.html', {'seance': seance, 'is_coach': is_coach})