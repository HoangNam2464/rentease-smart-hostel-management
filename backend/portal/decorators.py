from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


def is_admin_user(user):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.is_staff
            or getattr(user, 'is_rentease_admin', False)
            or getattr(user, 'user_type', None) == 'ADMIN'
        )
    )


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path(), login_url='/login/')

            if is_admin_user(request.user) or getattr(request.user, 'user_type', None) in roles:
                return view_func(request, *args, **kwargs)

            return redirect('portal:access_denied')

        return wrapped

    return decorator


owner_required = role_required('OWNER')
tenant_required = role_required('TENANT')
