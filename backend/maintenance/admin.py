from django.contrib import admin
from django.utils import timezone

from .models import MaintenanceRecord, Notification, RepairRequest


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ['room', 'tenant', 'title', 'priority', 'status', 'requested_at', 'resolved_at']
    search_fields = [
        'title',
        'description',
        'room__room_code',
        'room__room_name',
        'tenant__full_name',
        'tenant__phone_number',
    ]
    list_filter = ['status', 'priority', 'requested_at', 'room__owner']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['room', 'room__owner', 'tenant']
    actions = ['mark_in_progress', 'mark_completed', 'mark_cancelled']

    @admin.action(description='Mark selected requests as in progress')
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status=RepairRequest.STATUS_IN_PROGRESS, resolved_at=None)
        self.message_user(request, f'Marked {updated} repair requests as in progress.')

    @admin.action(description='Mark selected requests as completed')
    def mark_completed(self, request, queryset):
        updated = queryset.update(status=RepairRequest.STATUS_COMPLETED, resolved_at=timezone.now())
        self.message_user(request, f'Marked {updated} repair requests as completed.')

    @admin.action(description='Mark selected requests as cancelled')
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status=RepairRequest.STATUS_CANCELLED, resolved_at=None)
        self.message_user(request, f'Marked {updated} repair requests as cancelled.')


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = [
        'room',
        'maintenance_type',
        'vendor_name',
        'status',
        'cost',
        'scheduled_for',
        'completed_at',
        'performed_by',
    ]
    search_fields = [
        'room__room_code',
        'room__room_name',
        'description',
        'vendor_name',
        'performed_by',
    ]
    list_filter = ['status', 'maintenance_type', 'scheduled_for', 'completed_at']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['room', 'repair_request']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'title', 'notification_type', 'is_read', 'created_at', 'read_at']
    search_fields = [
        'tenant__full_name',
        'tenant__phone_number',
        'title',
        'message',
        'invoice__invoice_code',
    ]
    list_filter = ['notification_type', 'is_read', 'created_at']
    readonly_fields = ['created_at']
    list_select_related = ['tenant', 'invoice', 'repair_request']
    actions = ['mark_read', 'mark_unread']

    @admin.action(description='Mark selected notifications as read')
    def mark_read(self, request, queryset):
        updated = queryset.update(is_read=True, read_at=timezone.now())
        self.message_user(request, f'Marked {updated} notifications as read.')

    @admin.action(description='Mark selected notifications as unread')
    def mark_unread(self, request, queryset):
        updated = queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'Marked {updated} notifications as unread.')
