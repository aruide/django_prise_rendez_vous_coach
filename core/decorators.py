routes = []

def route(path, name=""):
    def decorator(obj):
        # Si c'est une classe Django CBV (possède as_view)
        if hasattr(obj, 'as_view'):
            routes.append((path, obj.as_view(), name))
        else:
            routes.append((path, obj, name))
        return obj
    return decorator