from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path('dashboard/', views.dashboard, name='dashboard'),
   path('prendre-rdv/', views.prendre_rdv, name='prendre_rdv'),
   path("seance/<int:seance_id>/", views.seance_detail, name="seance_detail"),

]
