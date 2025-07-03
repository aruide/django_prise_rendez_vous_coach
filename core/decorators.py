from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse_lazy

def logout_required(function=None, redirect_url=None):
    if redirect_url is None:
        redirect_url = reverse_lazy('accueil')  # Convertit le nom de vue en URL

    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=redirect_url,
        redirect_field_name=None
    )

    if function:
        return actual_decorator(function)
    return actual_decorator