from django.urls import path
from core.decorators import routes
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path('', views.accueil, name='accueil'),
   path('info/', views.info, name='info'),
   path('objectif/', views.objectif, name='objectif'),
]