from django.urls import path
from core.decorators import routes
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/',  auth_views.LogoutView.as_view(), name='logout'),
    path("mon-compte/", views.mon_compte, name="mon compte"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
