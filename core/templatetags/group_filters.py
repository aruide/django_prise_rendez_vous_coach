from django import template

register = template.Library()

# verifier si la personne appartient au groupe demande
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
