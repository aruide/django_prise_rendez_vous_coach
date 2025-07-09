from django import forms
from .models import Seance
from datetime import datetime, timedelta

class SeanceForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['date', 'heure_debut', 'objet']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'objet': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        heure = cleaned_data.get('heure_debut')

        if date and heure:
            now = datetime.now().date()

            # Pas de date dans le passé
            if date < now:
                raise forms.ValidationError("La date ne peut pas être dans le passé.")

            # Heures autorisées : 08:00 → 20:00
            if not (8 <= heure.hour < 20):
                raise forms.ValidationError("Les rendez-vous doivent être entre 08h00 et 20h00.")

            # Vérifier qu’il n’y a pas de séance existante au même créneau
            from .models import Seance
            if Seance.objects.filter(date=date, heure_debut=heure).exists():
                raise forms.ValidationError("Ce créneau est déjà réservé.")

            # Vérifier écart minimal de 10 minutes
            from datetime import timedelta
            debut_min = (datetime.combine(date, heure) - timedelta(minutes=10)).time()
            debut_max = (datetime.combine(date, heure) + timedelta(minutes=10)).time()

            overlapping = Seance.objects.filter(
                date=date,
                heure_debut__gte=debut_min,
                heure_debut__lte=debut_max
            )
            if overlapping.exists():
                raise forms.ValidationError("Un autre rendez-vous est trop proche (10 min).")

        return cleaned_data

class AnnulationForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['motif_annulation']
        widgets = {
            'motif_annulation': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def clean_motif_annulation(self):
        motif = self.cleaned_data.get('motif_annulation', '').strip()
        if not motif:
            raise forms.ValidationError("Vous devez saisir un motif d'annulation.")
        return motif
