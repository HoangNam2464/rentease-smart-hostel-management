from django.contrib import admin

from .models import Invoice, InvoiceDetail, PaymentHistory, PriceConfig


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

    @admin.action(description='Recalculate selected invoices')
    def recalculate_selected_invoices(self, request, queryset):
        for invoice in queryset:
            invoice.recalculate_totals()
        self.message_user(request, f'Recalculated {queryset.count()} invoices.')

    @admin.action(description='Mark selected invoices as overdue')
    def mark_selected_overdue(self, request, queryset):
        updated = queryset.exclude(status=Invoice.STATUS_PAID).update(status=Invoice.STATUS_OVERDUE)
        self.message_user(request, f'Marked {updated} invoices as overdue.')


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
