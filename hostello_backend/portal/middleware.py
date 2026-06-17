import os

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect


def auto_auth_bypass_enabled():
    return settings.DEBUG and os.environ.get('RENTEASE_AUTO_AUTH_BYPASS') == '1'


class DevAutoAuthBypassMiddleware:
    """Development-only role auto-login for local RentEase testing."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if auto_auth_bypass_enabled():
            response = self._maybe_auto_authenticate(request)
            if response is not None:
                return response

        return self.get_response(request)

    def _maybe_auto_authenticate(self, request):
        path = request.path_info

        if path in ('/login/', '/register/'):
            if self._login_role_user(request, 'OWNER'):
                return redirect('/dashboard/')
            return redirect('/')

        if path == '/dashboard/' and self._login_role_user(request, 'OWNER'):
            return None

        if path.startswith('/owner/'):
            self._login_role_user(request, 'OWNER')
        elif path.startswith('/tenant/'):
            self._login_role_user(request, 'TENANT')
        elif path.startswith('/admin/') or path.startswith('/reports/'):
            self._login_staff_user(request)

        return None

    def _login_role_user(self, request, role):
        User = get_user_model()
        related_profile = 'rentease_profile' if role == 'OWNER' else 'tenant_profile'
        user = (
            User.objects
            .filter(user_type=role, is_active=True, **{f'{related_profile}__isnull': False})
            .first()
        )
        return self._login_user(request, user)

    def _login_staff_user(self, request):
        User = get_user_model()
        user = User.objects.filter(is_staff=True, is_active=True).order_by('-is_superuser', 'id').first()
        return self._login_user(request, user)

    def _login_user(self, request, user):
        if user is None:
            return False

        if request.user.is_authenticated and request.user.pk == user.pk:
            return True

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return True
