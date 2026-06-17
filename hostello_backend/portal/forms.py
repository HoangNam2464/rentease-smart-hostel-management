from django import forms
from django.contrib.auth.forms import AuthenticationForm

from maintenance.models import RepairRequest


class RentEaseAuthenticationForm(AuthenticationForm):
    """Login form for the RentEase role-based portal."""

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': (
            'Please enter a correct username and password. Note that both '
            'fields may be case-sensitive.'
        ),
    }


class TenantRepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ['room', 'title', 'description', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, allowed_rooms=None, **kwargs):
        super().__init__(*args, **kwargs)
        room_model = RepairRequest._meta.get_field('room').remote_field.model
        self.allowed_rooms = allowed_rooms if allowed_rooms is not None else room_model.objects.none()
        self.fields['room'].queryset = self.allowed_rooms
        self.fields['room'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['priority'].required = True

    def clean_room(self):
        room = self.cleaned_data['room']
        if not self.allowed_rooms.filter(pk=room.pk).exists():
            raise forms.ValidationError('Selected room is not linked to your active contracts.')
        return room
