from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SeanceForm, AnnulationForm
from .models import Seance
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .services.seance_services import is_user_coach, get_user_seances, split_seances_future_past, user_can_view_seance, update_note_coach, annuler_seance_instance

@login_required
def dashboard(request):
    seances = get_user_seances(request.user)
    seances_avenir, seances_passees = split_seances_future_past(seances)

    context = {
        'seances_avenir': Paginator(seances_avenir, 5).get_page(request.GET.get('page_avenir')),
        'seances_passees': Paginator(seances_passees, 5).get_page(request.GET.get('page_passees')),
        'user': request.user,
    }

    template = 'rdv/dashboard_coach.html' if is_user_coach(request.user) else 'rdv/dashboard_client.html'
    return render(request, template, context)


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

    if not user_can_view_seance(request.user, seance):
        return render(request, '403.html', status=403)

    is_coach = is_user_coach(request.user)

    if request.method == 'POST' and is_coach:
        update_note_coach(seance, request.POST.get('note_coach'))
        return redirect('seance_detail', seance_id=seance.id)

    return render(request, 'rdv/seance_detail.html', {'seance': seance, 'is_coach': is_coach})

@login_required
def annuler_seance(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)

    if request.method == 'POST':
        form = AnnulationForm(request.POST, instance=seance)
        if form.is_valid():
            form.save(commit=False)
            annuler_seance_instance(seance)
            messages.success(request, "La séance a été annulée.")
            return redirect('dashboard')
    else:
        form = AnnulationForm(instance=seance)

    return render(request, 'rdv/annule_seance.html', {
        'form': form,
        'seance': seance
    })