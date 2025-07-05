from django.shortcuts import render

# Create your views here.
from core.decorators import route

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def accueil(request):
    return render(request, "siteweb/accueil.html")

def info(request):
    return render(request, "siteweb/info.html")

def objectif(request):
    return render(request, "siteweb/objectif.html")