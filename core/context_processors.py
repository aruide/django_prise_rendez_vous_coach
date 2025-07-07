def photo_utilisateur(request):
    if request.user.is_authenticated:
        try:
            return {'photo_utilisateur': request.user.photo}
        except:
            return {'photo_utilisateur': None}
    return {}