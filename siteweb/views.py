from django.shortcuts import render

from django.contrib.auth import get_user_model

def accueil(request):
    return render(request, "siteweb/accueil.html")

def info(request):
    return render(request, "siteweb/info.html")

def objectif(request):
    return render(request, "siteweb/objectif.html")

def equipe(request):
    User = get_user_model()
    coachs = User.objects.filter(groups__name__in=["coach", "coach admin"]).distinct()    
    return render(request, "siteweb/equipe.html", {'coachs': coachs})