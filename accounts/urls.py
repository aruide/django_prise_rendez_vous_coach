from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/',  auth_views.LogoutView.as_view(), name='logout'),
    path("mon-compte/", views.mon_compte, name="mon compte"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
