from django.contrib import admin

from .models import CoTenant, Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    SENSITIVE_TENANT_FIELDS = ['citizen_id', 'citizen_id_front', 'citizen_id_back']

    list_display = ['full_name', 'phone_number', 'email', 'status', 'created_at']
    list_filter = ['status', 'gender', 'created_at']
    search_fields = ['full_name', 'phone_number', 'email', 'account__username']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['account']

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly += self.SENSITIVE_TENANT_FIELDS
        return readonly
    fieldsets = (
        ('Tenant profile', {
            'fields': (
                'account',
                'full_name',
                'email',
                'phone_number',
                'status',
                'address',
                'date_of_birth',
                'gender',
            )
        }),
        ('Sensitive identity data', {
            'classes': ('collapse',),
            'fields': (
                'citizen_id',
                'citizen_id_front',
                'citizen_id_back',
            )
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )


@admin.register(CoTenant)
class CoTenantAdmin(admin.ModelAdmin):
    SENSITIVE_COTENANT_FIELDS = ['citizen_id']

    list_display = ['full_name', 'contract', 'phone_number', 'relationship']
    list_filter = ['relationship']
    search_fields = ['full_name', 'phone_number', 'contract__contract_code']
    list_select_related = ['contract']

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly += self.SENSITIVE_COTENANT_FIELDS
        return readonly
    fieldsets = (
        ('Co-tenant profile', {
            'fields': (
                'contract',
                'full_name',
                'phone_number',
                'relationship',
            )
        }),
        ('Sensitive identity data', {
            'classes': ('collapse',),
            'fields': (
                'citizen_id',
            )
        }),
    )
