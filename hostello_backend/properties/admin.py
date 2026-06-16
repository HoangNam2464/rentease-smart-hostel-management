from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_code', 'room_name', 'owner', 'floor', 'default_rent', 'status', 'updated_at']
    list_filter = ['status', 'floor', 'owner']
    search_fields = ['room_code', 'room_name', 'owner__full_name', 'owner__user__username']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['owner', 'owner__user']
