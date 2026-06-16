from django.contrib import admin

from .models import CoTenant, Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'citizen_id', 'phone_number', 'email', 'status', 'created_at']
    list_filter = ['status', 'gender', 'created_at']
    search_fields = ['full_name', 'citizen_id', 'phone_number', 'email', 'account__username']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['account']


@admin.register(CoTenant)
class CoTenantAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'contract', 'phone_number', 'citizen_id', 'relationship']
    list_filter = ['relationship']
    search_fields = ['full_name', 'citizen_id', 'phone_number', 'contract__contract_code']
    list_select_related = ['contract']
