from django import forms
from django.contrib import admin
from django.db.models import Count

from .models import Property, Room


class RoomAdminForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['property'].required = True

    def clean(self):
        cleaned_data = super().clean()
        owner = cleaned_data.get('owner')
        property_record = cleaned_data.get('property')
        if owner and property_record and property_record.owner_id != owner.pk:
            self.add_error('property', 'Cơ sở cho thuê phải thuộc cùng chủ trọ với phòng.')
        return cleaned_data


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['property_code', 'name', 'owner', 'province_city', 'room_count', 'status', 'updated_at']
    list_filter = ['status', 'province_city', 'owner']
    search_fields = [
        'property_code',
        'name',
        'address',
        'ward',
        'province_city',
        'owner__full_name',
        'owner__user__username',
    ]
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['owner', 'owner__user']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_room_count=Count('rooms'))

    @admin.display(description='Rooms', ordering='_room_count')
    def room_count(self, obj):
        return obj._room_count

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj:
            readonly.extend(['owner', 'property_code'])
        return readonly


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    list_display = ['room_code', 'room_name', 'property', 'owner', 'floor', 'default_rent', 'status', 'updated_at']
    list_filter = ['status', 'floor', 'property', 'owner']
    search_fields = [
        'room_code',
        'room_name',
        'property__property_code',
        'property__name',
        'owner__full_name',
        'owner__user__username',
    ]
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['property', 'property__owner', 'owner', 'owner__user']
