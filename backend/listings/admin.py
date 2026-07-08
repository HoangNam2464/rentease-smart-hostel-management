from django.contrib import admin
from django.utils import timezone

from .models import RoomListing, ViewingRegistration


@admin.register(RoomListing)
class RoomListingAdmin(admin.ModelAdmin):
    list_display = ['room', 'title', 'listing_price', 'deposit_amount', 'status', 'available_from', 'published_at']
    search_fields = ['title', 'description', 'room__room_code', 'room__room_name']
    list_filter = ['status', 'available_from', 'published_at']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['room', 'room__owner']
    actions = ['mark_published', 'mark_hidden', 'mark_expired']

    @admin.action(description='Đánh dấu tin đã đăng')
    def mark_published(self, request, queryset):
        updated = 0
        for listing in queryset:
            listing.status = RoomListing.STATUS_PUBLISHED
            listing.save()
            updated += 1
        self.message_user(request, f'Đã đánh dấu {updated} tin là đã đăng.')

    @admin.action(description='Đánh dấu tin đã ẩn')
    def mark_hidden(self, request, queryset):
        updated = queryset.update(status=RoomListing.STATUS_HIDDEN)
        self.message_user(request, f'Đã đánh dấu {updated} tin là đã ẩn.')

    @admin.action(description='Đánh dấu tin đã hết hạn')
    def mark_expired(self, request, queryset):
        updated = queryset.update(status=RoomListing.STATUS_EXPIRED, expired_at=timezone.now())
        self.message_user(request, f'Đã đánh dấu {updated} tin là đã hết hạn.')


@admin.register(ViewingRegistration)
class ViewingRegistrationAdmin(admin.ModelAdmin):
    list_display = ['listing', 'full_name', 'phone', 'preferred_date', 'preferred_time', 'status', 'created_at']
    search_fields = [
        'full_name',
        'phone',
        'email',
        'listing__title',
        'listing__room__room_code',
        'listing__room__room_name',
    ]
    list_filter = ['status', 'preferred_date', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['listing', 'listing__room', 'tenant']
    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled', 'mark_no_show']

    @admin.action(description='Đánh dấu đăng ký đã xác nhận')
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status=ViewingRegistration.STATUS_CONFIRMED)
        self.message_user(request, f'Đã đánh dấu {updated} đăng ký là đã xác nhận.')

    @admin.action(description='Đánh dấu đăng ký đã hoàn thành')
    def mark_completed(self, request, queryset):
        updated = queryset.update(status=ViewingRegistration.STATUS_COMPLETED)
        self.message_user(request, f'Đã đánh dấu {updated} đăng ký là đã hoàn thành.')

    @admin.action(description='Đánh dấu đăng ký đã hủy')
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status=ViewingRegistration.STATUS_CANCELLED)
        self.message_user(request, f'Đã đánh dấu {updated} đăng ký là đã hủy.')

    @admin.action(description='Đánh dấu đăng ký không đến')
    def mark_no_show(self, request, queryset):
        updated = queryset.update(status=ViewingRegistration.STATUS_NO_SHOW)
        self.message_user(request, f'Đã đánh dấu {updated} đăng ký là không đến.')
