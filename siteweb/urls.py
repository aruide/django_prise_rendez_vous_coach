from django.urls import path
from . import views

urlpatterns = [
   path('', views.accueil, name='accueil'),
   path('info/', views.info, name='info'),
   path('objectif/', views.objectif, name='objectif'),
   path('equipe/', views.equipe, name='equipe'),
]