from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

"""
    Envoie un email d'activation de compte à un utilisateur nouvellement inscrit.

    L'email contient un lien d'activation unique généré via un token et encodé.
    Le contenu est envoyé en texte brut et en HTML.

    Args:
        user (User): L'utilisateur auquel l'email d'activation doit être envoyé.
                     L'objet doit avoir au minimum les attributs `username` et `email`.
        activation_url (str): L'URL complète d'activation contenant le token.

    Returns:
        None
"""
def send_activation_email(user, activation_url):
    subject = "Confirmez votre inscription"
    from_email = 'noreply@monsite.fr'
    to_email = [user.email]

    text_content = f"Bonjour {user.username}, cliquez ici pour activer votre compte : {activation_url}"

    html_content = render_to_string("accounts/activation_email.html", {
        'user': user,
        'activation_url': activation_url
    })

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()
