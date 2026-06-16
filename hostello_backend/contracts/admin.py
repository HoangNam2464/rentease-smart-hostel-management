from django.contrib import admin

from tenants.models import CoTenant
from .models import Contract


class CoTenantInline(admin.TabularInline):
    model = CoTenant
    extra = 0


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['contract_code', 'room', 'tenant', 'start_date', 'end_date', 'rent_amount', 'status']
    list_filter = ['status', 'payment_cycle', 'start_date', 'end_date']
    search_fields = ['contract_code', 'room__room_code', 'room__room_name', 'tenant__full_name', 'tenant__citizen_id']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['room', 'tenant', 'previous_contract']
    inlines = [CoTenantInline]
