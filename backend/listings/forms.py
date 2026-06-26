from django import forms

from .models import ViewingRegistration


class ViewingRegistrationForm(forms.ModelForm):
    class Meta:
        model = ViewingRegistration
        fields = ['full_name', 'phone', 'email', 'preferred_date', 'preferred_time', 'note']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'type': 'time'}),
            'note': forms.Textarea(attrs={'rows': 4}),
        }
