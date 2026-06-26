from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, WardenProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'is_active']
    list_filter = ['user_type', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('RentEase Info', {
            'fields': ('user_type', 'phone_number', 'email', 'first_name', 'last_name')
        }),
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'phone_number', 'rental_address', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['full_name', 'phone_number', 'user__username', 'user__email', 'rental_address']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(WardenProfile)
class WardenProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'designation', 'department', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'designation']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
