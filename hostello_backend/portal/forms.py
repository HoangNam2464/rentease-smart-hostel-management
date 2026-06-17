from django.contrib.auth.forms import AuthenticationForm


class RentEaseAuthenticationForm(AuthenticationForm):
    """Login form for the RentEase role-based portal."""

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': (
            'Please enter a correct username and password. Note that both '
            'fields may be case-sensitive.'
        ),
    }
