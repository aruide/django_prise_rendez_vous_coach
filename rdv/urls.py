from django.urls import path
from core.decorators import routes
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path('', views.accueil, name='accueil'),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('prendre-rdv/', views.prendre_rdv, name='prendre_rdv'),
]
