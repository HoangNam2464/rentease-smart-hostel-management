from django.contrib import admin

from .models import (
    Invoice,
    InvoiceDetail,
    InvoiceLine,
    Meter,
    MeterReading,
    PaymentHistory,
    PriceConfig,
    ServiceDefinition,
)


@admin.register(PriceConfig)
class PriceConfigAdmin(admin.ModelAdmin):
    list_display = [
        'room',
        'month',
        'year',
        'electricity_unit_price',
        'water_unit_price',
        'service_fee',
        'effective_from',
        'updated_at',
    ]
    search_fields = ['room__room_code', 'room__room_name', 'room__owner__full_name']
    list_filter = ['year', 'month', 'room__owner']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['room', 'room__owner']


@admin.register(ServiceDefinition)
class ServiceDefinitionAdmin(admin.ModelAdmin):
    list_display = [
        'service_code',
        'name',
        'property',
        'charge_method',
        'unit',
        'default_unit_price',
        'is_active',
        'updated_at',
    ]
    search_fields = ['service_code', 'name', 'property__property_code', 'property__name']
    list_filter = ['charge_method', 'is_active', 'property__owner']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['property', 'property__owner']


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = [
        'meter_code',
        'room',
        'service_definition',
        'serial_number',
        'initial_value',
        'is_active',
        'installed_on',
        'retired_on',
    ]
    search_fields = [
        'meter_code',
        'serial_number',
        'room__room_code',
        'room__room_name',
        'service_definition__service_code',
    ]
    list_filter = ['is_active', 'service_definition__charge_method', 'room__property']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['room', 'room__property', 'service_definition']


@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = [
        'meter',
        'month',
        'year',
        'previous_value',
        'current_value',
        'consumption',
        'read_at',
        'captured_by',
    ]
    search_fields = ['meter__meter_code', 'meter__serial_number', 'meter__room__room_code']
    list_filter = ['year', 'month', 'meter__room__property']
    readonly_fields = ['consumption', 'created_at', 'updated_at']
    list_select_related = ['meter', 'meter__room', 'captured_by']


class InvoiceDetailInline(admin.StackedInline):
    model = InvoiceDetail
    extra = 0
    max_num = 1
    can_delete = False
    fields = [
        'electricity_start',
        'electricity_end',
        'water_start',
        'water_end',
        'electricity_unit_price',
        'water_unit_price',
        'electricity_amount',
        'water_amount',
        'rent_amount',
        'service_amount',
    ]
    readonly_fields = [
        'electricity_unit_price',
        'water_unit_price',
        'electricity_amount',
        'water_amount',
        'rent_amount',
        'service_amount',
    ]


class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0
    fields = ['amount', 'method', 'transaction_code', 'paid_at', 'collector', 'note', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_code',
        'contract',
        'month',
        'year',
        'total_amount',
        'paid_amount',
        'remaining_amount',
        'status',
        'due_date',
    ]
    search_fields = [
        'invoice_code',
        'contract__contract_code',
        'contract__tenant__full_name',
        'contract__tenant__phone_number',
        'contract__tenant__email',
        'contract__room__room_code',
        'contract__room__room_name',
    ]
    list_filter = ['status', 'year', 'month', 'due_date', 'contract__room__owner']
    readonly_fields = [
        'invoice_code',
        'total_amount',
        'paid_amount',
        'remaining_amount',
        'created_at',
        'updated_at',
    ]
    list_select_related = ['contract', 'contract__tenant', 'contract__room']
    inlines = [InvoiceDetailInline, PaymentHistoryInline]
    actions = ['recalculate_selected_invoices', 'mark_selected_overdue']

    @admin.action(description='Tính lại hóa đơn đã chọn')
    def recalculate_selected_invoices(self, request, queryset):
        for invoice in queryset:
            invoice.recalculate_totals()
        self.message_user(request, f'Đã tính lại {queryset.count()} hóa đơn.')

    @admin.action(description='Đánh dấu hóa đơn đã chọn là quá hạn')
    def mark_selected_overdue(self, request, queryset):
        updated = queryset.exclude(status=Invoice.STATUS_PAID).update(status=Invoice.STATUS_OVERDUE)
        self.message_user(request, f'Đã đánh dấu {updated} hóa đơn là quá hạn.')


@admin.register(InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):
    list_display = [
        'invoice',
        'line_code',
        'line_type',
        'direction',
        'description',
        'quantity',
        'unit_price',
        'amount',
        'sort_order',
    ]
    search_fields = [
        'invoice__invoice_code',
        'line_code',
        'description',
        'invoice__contract__room__room_code',
    ]
    list_filter = ['line_type', 'direction', 'invoice__year', 'invoice__month']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = [
        'invoice',
        'invoice__contract',
        'service_definition',
        'meter_reading',
        'legacy_detail',
    ]


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'amount', 'method', 'transaction_code', 'paid_at', 'collector', 'created_at']
    search_fields = [
        'invoice__invoice_code',
        'invoice__contract__contract_code',
        'invoice__contract__tenant__full_name',
        'transaction_code',
        'collector__username',
    ]
    list_filter = ['method', 'paid_at', 'collector']
    readonly_fields = ['created_at']
    list_select_related = ['invoice', 'invoice__contract', 'collector']
