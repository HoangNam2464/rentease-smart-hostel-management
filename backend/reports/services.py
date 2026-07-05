from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, Sum
from django.utils import timezone

from billing.models import Invoice
from contracts.models import Contract
from listings.models import RoomListing, ViewingRegistration
from maintenance.models import MaintenanceRecord, RepairRequest
from properties.models import Property, Room
from tenants.models import Tenant


ZERO = Decimal('0.00')


def money_sum(queryset, field_name):
    return queryset.aggregate(total=Sum(field_name))['total'] or ZERO


def count_by_status(queryset):
    return {row['status']: row['count'] for row in queryset.values('status').annotate(count=Count('id'))}


def current_month_year():
    today = timezone.localdate()
    return today.month, today.year


def dashboard_metrics():
    month, year = current_month_year()
    current_month_invoices = Invoice.objects.filter(month=month, year=year)

    return {
        'month': month,
        'year': year,
        'total_rooms': Room.objects.count(),
        'available_rooms': Room.objects.filter(status='available').count(),
        'occupied_rooms': Room.objects.filter(status='occupied').count(),
        'total_tenants': Tenant.objects.count(),
        'active_contracts': Contract.objects.filter(status='active').count(),
        'monthly_invoice_total': money_sum(current_month_invoices, 'total_amount'),
        'paid_amount_this_month': money_sum(current_month_invoices, 'paid_amount'),
        'outstanding_debt': money_sum(Invoice.objects.all(), 'remaining_amount'),
        'pending_repair_requests': RepairRequest.objects.filter(status=RepairRequest.STATUS_PENDING).count(),
        'published_room_listings': RoomListing.objects.filter(status=RoomListing.STATUS_PUBLISHED).count(),
        'pending_viewing_registrations': ViewingRegistration.objects.filter(status=ViewingRegistration.STATUS_PENDING).count(),
    }


def billing_report(month=None, year=None, status=None):
    current_month, current_year = current_month_year()
    month = int(month or current_month)
    year = int(year or current_year)

    invoices = Invoice.objects.select_related('contract', 'contract__room', 'contract__tenant').filter(
        month=month,
        year=year,
    )
    if status:
        invoices = invoices.filter(status=status)

    return {
        'month': month,
        'year': year,
        'status': status or '',
        'status_choices': Invoice.STATUS_CHOICES,
        'invoices': invoices.order_by('contract__room__room_code', 'invoice_code'),
        'total_invoice_amount': money_sum(invoices, 'total_amount'),
        'paid_amount': money_sum(invoices, 'paid_amount'),
        'remaining_debt': money_sum(invoices, 'remaining_amount'),
    }


def property_filter_context(property_id):
    properties = Property.objects.select_related('owner').order_by('owner__full_name', 'property_code')
    try:
        selected_property = properties.filter(pk=property_id).first() if property_id else None
    except (TypeError, ValueError):
        selected_property = None
    return properties, selected_property


def room_report(property_id=None):
    properties, selected_property = property_filter_context(property_id)
    rooms = Room.objects.select_related('owner', 'property')
    if selected_property:
        rooms = rooms.filter(property=selected_property)
    rooms = rooms.order_by('property__property_code', 'room_code')
    status_summary = count_by_status(rooms)
    active_contract_room_ids = Contract.objects.filter(
        status='active',
        room__in=rooms,
    ).values_list('room_id', flat=True).distinct()

    return {
        'rooms': rooms,
        'status_summary': status_summary,
        'total_rooms': rooms.count(),
        'active_contract_room_count': active_contract_room_ids.count(),
        'available_rooms': status_summary.get('available', 0),
        'occupied_rooms': status_summary.get('occupied', 0),
        'maintenance_rooms': status_summary.get('maintenance', 0),
        'inactive_rooms': status_summary.get('inactive', 0),
        'properties': properties,
        'selected_property': selected_property,
    }


def tenant_contract_report():
    today = timezone.localdate()
    ending_soon_date = today + timedelta(days=30)
    active_contracts = Contract.objects.select_related('room', 'tenant').filter(status='active')

    return {
        'active_tenants': Tenant.objects.filter(status='active').order_by('full_name'),
        'active_contracts': active_contracts.order_by('end_date'),
        'contracts_ending_soon': active_contracts.filter(end_date__gte=today, end_date__lte=ending_soon_date).order_by('end_date'),
        'ending_soon_days': 30,
    }


def maintenance_report():
    completed_records = MaintenanceRecord.objects.filter(status=MaintenanceRecord.STATUS_COMPLETED)

    return {
        'pending_repair_requests': RepairRequest.objects.select_related('room', 'tenant').filter(
            status=RepairRequest.STATUS_PENDING,
        ).order_by('-requested_at'),
        'completed_maintenance_records': completed_records.select_related('room', 'repair_request').order_by('-completed_at'),
        'maintenance_cost_summary': money_sum(completed_records, 'cost'),
    }


def listing_report(property_id=None):
    properties, selected_property = property_filter_context(property_id)
    listings = RoomListing.objects.select_related('room', 'room__property')
    registrations = ViewingRegistration.objects.select_related(
        'listing',
        'listing__room',
        'listing__room__property',
        'tenant',
    )
    if selected_property:
        listings = listings.filter(room__property=selected_property)
        registrations = registrations.filter(listing__room__property=selected_property)

    return {
        'properties': properties,
        'selected_property': selected_property,
        'published_listings': listings.filter(
            status=RoomListing.STATUS_PUBLISHED,
        ).order_by('-published_at'),
        'pending_viewing_registrations': registrations.filter(
            status=ViewingRegistration.STATUS_PENDING,
        ).order_by('preferred_date', 'preferred_time'),
        'completed_viewings': registrations.filter(
            status=ViewingRegistration.STATUS_COMPLETED,
        ).order_by('-updated_at'),
        'no_show_viewings': registrations.filter(
            status=ViewingRegistration.STATUS_NO_SHOW,
        ).order_by('-updated_at'),
    }
