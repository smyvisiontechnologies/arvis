from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def get_user_role(user):
    profile = getattr(user, "profile", None)

    if profile:
        return profile.role

    return None


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            role = get_user_role(request.user)

            if request.user.is_superuser or role in allowed_roles:
                return view_func(request, *args, **kwargs)

            messages.error(request, "You do not have permission to access this page.")
            return redirect("dashboard")

        return wrapper

    return decorator