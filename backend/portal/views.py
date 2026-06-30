from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from billing.models import Invoice, PaymentHistory
from contracts.models import Contract
from listings.models import RoomListing, ViewingRegistration
from maintenance.models import Notification, RepairRequest
from properties.models import Property, Room
from tenants.models import Tenant

from .decorators import is_admin_user, owner_required, tenant_required
from .forms import (
    OwnerContractCreateForm,
    OwnerContractUpdateForm,
    OwnerInvoiceCreateForm,
    OwnerInvoiceUpdateForm,
    OwnerPaymentCreateForm,
    OwnerPropertyForm,
    OwnerRepairProcessForm,
    OwnerRoomForm,
    OwnerRoomListingForm,
    OwnerTenantForm,
    OwnerViewingRegistrationProcessForm,
    RentEaseAuthenticationForm,
    TenantRepairRequestForm,
)


MONEY_ZERO = Decimal('0.00')


def _choice_value(choices, label, fallback):
    for value, display in choices:
        if display == label:
            return value
    return fallback


def _money_sum(queryset, field_name):
    return queryset.aggregate(total=Sum(field_name))['total'] or MONEY_ZERO


def get_role_redirect_url(user):
    if is_admin_user(user):
        return '/admin/'
    if getattr(user, 'is_owner', False) or getattr(user, 'user_type', None) == 'OWNER':
        return '/owner/dashboard/'
    if getattr(user, 'is_tenant', False) or getattr(user, 'user_type', None) == 'TENANT':
        return '/tenant/dashboard/'
    return '/access-denied/'


def get_owner_profile(user):
    try:
        return user.rentease_profile
    except ObjectDoesNotExist:
        return None


def render_missing_owner_profile(request):
    return render(request, 'portal/owner_dashboard.html', {
        'missing_profile': True,
        'message': 'Owner profile is not linked yet.',
    })


def get_tenant_profile(user):
    try:
        return user.tenant_profile
    except ObjectDoesNotExist:
        return None


def render_missing_tenant_profile(request):
    return render(request, 'portal/tenant_dashboard.html', {
        'missing_profile': True,
        'message': 'Tenant profile is not linked yet.',
    })


def owner_rooms_queryset(profile):
    return Room.objects.select_related('property').filter(owner=profile)


def owner_properties_queryset(profile):
    return Property.objects.filter(owner=profile)


def owner_contracts_queryset(profile):
    return Contract.objects.select_related('room', 'tenant').filter(room__owner=profile)


def owner_listings_queryset(profile):
    return RoomListing.objects.select_related('room').filter(room__owner=profile)


def owner_tenants_queryset(profile):
    return Tenant.objects.filter(contracts__room__owner=profile).distinct()


def is_tenant_shared_across_owners(tenant):
    return tenant.contracts.values('room__owner').distinct().count() > 1


def owner_invoices_queryset(profile):
    return (
        Invoice.objects
        .select_related('contract', 'contract__room', 'contract__tenant')
        .filter(contract__room__owner=profile)
    )


def owner_payments_queryset(profile):
    return (
        PaymentHistory.objects
        .select_related('invoice', 'invoice__contract', 'invoice__contract__room')
        .filter(invoice__contract__room__owner=profile)
    )


def owner_repairs_queryset(profile):
    return RepairRequest.objects.select_related('room', 'tenant').filter(room__owner=profile)


def owner_viewing_registrations_queryset(profile):
    return (
        ViewingRegistration.objects
        .select_related('listing', 'listing__room', 'tenant')
        .filter(listing__room__owner=profile)
    )


def tenant_contracts_queryset(tenant):
    return Contract.objects.select_related('room').filter(tenant=tenant)


def tenant_invoices_queryset(tenant):
    return (
        Invoice.objects
        .select_related('contract', 'contract__room')
        .filter(contract__tenant=tenant)
    )


def tenant_payments_queryset(tenant):
    return (
        PaymentHistory.objects
        .select_related('invoice', 'invoice__contract', 'invoice__contract__room')
        .filter(invoice__contract__tenant=tenant)
    )


def tenant_repairs_queryset(tenant):
    return RepairRequest.objects.select_related('room').filter(tenant=tenant)


def tenant_active_rooms_queryset(tenant):
    active_contract_status = _choice_value(Contract.STATUS_CHOICES, 'Active', 'active')
    return (
        Room.objects
        .filter(contracts__tenant=tenant, contracts__status=active_contract_status)
        .distinct()
        .order_by('room_code')
    )


def tenant_notifications_queryset(tenant):
    return (
        Notification.objects
        .select_related('invoice', 'repair_request')
        .filter(tenant=tenant)
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_role_redirect_url(request.user))

    form = RentEaseAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        auth_login(request, form.get_user())
        return redirect(get_role_redirect_url(form.get_user()))

    return render(request, 'portal/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Bạn đã đăng xuất an toàn.')
    return redirect('/')


@login_required(login_url='/login/')
def dashboard_redirect(request):
    return redirect(get_role_redirect_url(request.user))


@owner_required
def owner_dashboard(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    available_status = _choice_value(Room.STATUS_CHOICES, 'Available', 'available')
    occupied_status = _choice_value(Room.STATUS_CHOICES, 'Occupied', 'occupied')
    maintenance_status = _choice_value(Room.STATUS_CHOICES, 'Maintenance', 'maintenance')
    inactive_status = _choice_value(Room.STATUS_CHOICES, 'Inactive', 'inactive')
    active_contract_status = _choice_value(Contract.STATUS_CHOICES, 'Active', 'active')
    draft_contract_status = _choice_value(Contract.STATUS_CHOICES, 'Draft', 'draft')
    expired_contract_status = _choice_value(Contract.STATUS_CHOICES, 'Expired', 'expired')
    terminated_contract_status = _choice_value(Contract.STATUS_CHOICES, 'Terminated', 'terminated')
    today = timezone.localdate()
    ending_soon_date = today + timedelta(days=30)

    owner_rooms = owner_rooms_queryset(profile)
    owner_contracts = owner_contracts_queryset(profile)
    owner_invoices = owner_invoices_queryset(profile)
    owner_payments = owner_payments_queryset(profile)
    owner_repairs = owner_repairs_queryset(profile)
    owner_listings = owner_listings_queryset(profile)
    owner_viewing_registrations = owner_viewing_registrations_queryset(profile)
    contracts_ending_soon = owner_contracts.filter(
        status=active_contract_status,
        end_date__gte=today,
        end_date__lte=ending_soon_date,
    )

    metrics = {
        'total_rooms': owner_rooms.count(),
        'available_rooms': owner_rooms.filter(status=available_status).count(),
        'occupied_rooms': owner_rooms.filter(status=occupied_status).count(),
        'maintenance_rooms': owner_rooms.filter(status=maintenance_status).count(),
        'inactive_rooms': owner_rooms.filter(status=inactive_status).count(),
        'total_contracts': owner_contracts.count(),
        'active_contracts': owner_contracts.filter(status=active_contract_status).count(),
        'draft_contracts': owner_contracts.filter(status=draft_contract_status).count(),
        'expired_contracts': owner_contracts.filter(status=expired_contract_status).count(),
        'terminated_contracts': owner_contracts.filter(status=terminated_contract_status).count(),
        'contracts_ending_soon': contracts_ending_soon.count(),
        'total_invoices': owner_invoices.count(),
        'draft_invoices': owner_invoices.filter(status=Invoice.STATUS_DRAFT).count(),
        'unpaid_invoices': owner_invoices.filter(status=Invoice.STATUS_UNPAID).count(),
        'partial_invoices': owner_invoices.filter(status=Invoice.STATUS_PARTIAL).count(),
        'paid_invoices': owner_invoices.filter(status=Invoice.STATUS_PAID).count(),
        'overdue_invoices': owner_invoices.filter(status=Invoice.STATUS_OVERDUE).count(),
        'total_invoice_amount': _money_sum(owner_invoices, 'total_amount'),
        'paid_amount': _money_sum(owner_invoices, 'paid_amount'),
        'outstanding_debt': _money_sum(owner_invoices, 'remaining_amount'),
        'pending_repairs': owner_repairs.filter(status=RepairRequest.STATUS_PENDING).count(),
        'in_progress_repairs': owner_repairs.filter(status=RepairRequest.STATUS_IN_PROGRESS).count(),
        'completed_repairs': owner_repairs.filter(status=RepairRequest.STATUS_COMPLETED).count(),
        'cancelled_repairs': owner_repairs.filter(status=RepairRequest.STATUS_CANCELLED).count(),
        'published_listings': owner_listings.filter(status=RoomListing.STATUS_PUBLISHED).count(),
        'pending_viewing_registrations': owner_viewing_registrations.filter(status=ViewingRegistration.STATUS_PENDING).count(),
        'confirmed_viewing_registrations': owner_viewing_registrations.filter(status=ViewingRegistration.STATUS_CONFIRMED).count(),
        'completed_viewing_registrations': owner_viewing_registrations.filter(status=ViewingRegistration.STATUS_COMPLETED).count(),
        'cancelled_viewing_registrations': owner_viewing_registrations.filter(status=ViewingRegistration.STATUS_CANCELLED).count(),
        'no_show_viewing_registrations': owner_viewing_registrations.filter(status=ViewingRegistration.STATUS_NO_SHOW).count(),
    }

    recent = {
        'invoices': owner_invoices.order_by('-year', '-month', '-created_at')[:5],
        'payments': owner_payments.order_by('-paid_at', '-created_at')[:5],
        'pending_repairs': owner_repairs.filter(status=RepairRequest.STATUS_PENDING).order_by('-requested_at', '-created_at')[:5],
        'upcoming_contracts': contracts_ending_soon.order_by('end_date', 'contract_code')[:5],
        'pending_viewings': owner_viewing_registrations.filter(
            status=ViewingRegistration.STATUS_PENDING,
        ).order_by('preferred_date', 'preferred_time', '-created_at')[:5],
    }

    return render(request, 'portal/owner_dashboard.html', {
        'profile': profile,
        'metrics': metrics,
        'recent': recent,
        'ending_soon_days': 30,
    })


@owner_required
def owner_properties_list(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    properties = (
        owner_properties_queryset(profile)
        .annotate(room_count=Count('rooms'))
        .order_by('property_code')
    )
    return render(request, 'portal/owner_properties_list.html', {
        'profile': profile,
        'properties': properties,
    })


@owner_required
def owner_property_detail(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    property_record = get_object_or_404(owner_properties_queryset(profile), pk=pk)
    rooms = owner_rooms_queryset(profile).filter(property=property_record).order_by('room_code')
    return render(request, 'portal/owner_property_detail.html', {
        'profile': profile,
        'property_record': property_record,
        'rooms': rooms,
    })


@owner_required
def owner_property_create(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    if request.method == 'POST':
        form = OwnerPropertyForm(request.POST, owner_profile=profile)
        if form.is_valid():
            property_record = form.save(commit=False)
            property_record.owner = profile
            try:
                property_record.save()
            except IntegrityError:
                form.add_error('property_code', 'Bạn đã có một cơ sở sử dụng mã này.')
            else:
                messages.success(request, 'Đã tạo cơ sở cho thuê.')
                return redirect('portal:owner_properties_list')
    else:
        form = OwnerPropertyForm(owner_profile=profile)

    return render(request, 'portal/owner_property_form.html', {
        'profile': profile,
        'form': form,
        'form_title': 'Thêm cơ sở cho thuê',
        'submit_label': 'Tạo cơ sở',
    })


@owner_required
def owner_property_update(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    property_record = get_object_or_404(owner_properties_queryset(profile), pk=pk)
    if request.method == 'POST':
        form = OwnerPropertyForm(
            request.POST,
            instance=property_record,
            owner_profile=profile,
        )
        if form.is_valid():
            updated_property = form.save(commit=False)
            updated_property.owner = profile
            try:
                updated_property.save()
            except IntegrityError:
                form.add_error('property_code', 'Bạn đã có một cơ sở sử dụng mã này.')
            else:
                messages.success(request, 'Đã cập nhật cơ sở cho thuê.')
                return redirect('portal:owner_property_detail', pk=property_record.pk)
    else:
        form = OwnerPropertyForm(
            instance=property_record,
            owner_profile=profile,
        )

    return render(request, 'portal/owner_property_form.html', {
        'profile': profile,
        'property_record': property_record,
        'form': form,
        'form_title': 'Cập nhật cơ sở cho thuê',
        'submit_label': 'Lưu thay đổi',
    })


@owner_required
def owner_rooms_list(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    rooms = owner_rooms_queryset(profile).order_by('property__property_code', 'room_code')
    return render(request, 'portal/owner_rooms_list.html', {
        'profile': profile,
        'rooms': rooms,
    })


@owner_required
def owner_room_detail(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    room = get_object_or_404(owner_rooms_queryset(profile), pk=pk)
    return render(request, 'portal/owner_room_detail.html', {
        'profile': profile,
        'room': room,
    })


@owner_required
def owner_room_create(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    if request.method == 'POST':
        form = OwnerRoomForm(request.POST, owner_profile=profile)
        if form.is_valid():
            room = form.save(commit=False)
            room.owner = profile
            try:
                room.save()
            except ValidationError as exc:
                form.add_error(None, exc)
            except IntegrityError:
                form.add_error('room_code', 'Bạn đã có một phòng sử dụng mã này.')
            else:
                messages.success(request, 'Đã tạo phòng.')
                return redirect('portal:owner_rooms_list')
    else:
        form = OwnerRoomForm(owner_profile=profile)

    return render(request, 'portal/owner_room_form.html', {
        'profile': profile,
        'form': form,
        'has_properties': owner_properties_queryset(profile).exists(),
        'form_title': 'Thêm phòng',
        'submit_label': 'Tạo phòng',
    })


@owner_required
def owner_room_update(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    room = get_object_or_404(owner_rooms_queryset(profile), pk=pk)

    if request.method == 'POST':
        form = OwnerRoomForm(request.POST, instance=room, owner_profile=profile)
        if form.is_valid():
            updated_room = form.save(commit=False)
            updated_room.owner = profile
            try:
                updated_room.save()
            except ValidationError as exc:
                form.add_error(None, exc)
            except IntegrityError:
                form.add_error('room_code', 'Bạn đã có một phòng sử dụng mã này.')
            else:
                messages.success(request, 'Đã cập nhật phòng.')
                return redirect('portal:owner_room_detail', pk=room.pk)
    else:
        form = OwnerRoomForm(instance=room, owner_profile=profile)

    return render(request, 'portal/owner_room_form.html', {
        'profile': profile,
        'room': room,
        'form': form,
        'has_properties': owner_properties_queryset(profile).exists(),
        'form_title': 'Cập nhật phòng',
        'submit_label': 'Lưu thay đổi',
    })


@owner_required
def owner_contracts_list(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    contracts = owner_contracts_queryset(profile).order_by('-start_date', 'contract_code')
    return render(request, 'portal/owner_contracts_list.html', {
        'profile': profile,
        'contracts': contracts,
    })


@owner_required
def owner_contract_detail(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    contract = get_object_or_404(owner_contracts_queryset(profile), pk=pk)
    return render(request, 'portal/owner_contract_detail.html', {
        'profile': profile,
        'contract': contract,
    })


@owner_required
def owner_contract_create(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    if request.method == 'POST':
        form = OwnerContractCreateForm(request.POST, owner_profile=profile)
        if form.is_valid():
            try:
                contract = form.save()
            except ValidationError as exc:
                form.add_error(None, exc)
            except IntegrityError:
                form.add_error('contract_code', 'This contract code is already in use.')
            else:
                messages.success(request, 'Contract created successfully.')
                return redirect('portal:owner_contract_detail', pk=contract.pk)
    else:
        form = OwnerContractCreateForm(owner_profile=profile)

    return render(request, 'portal/owner_contract_form.html', {
        'profile': profile,
        'form': form,
        'form_title': 'Create Contract',
        'submit_label': 'Create Contract',
    })


@owner_required
def owner_contract_update(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    contract = get_object_or_404(owner_contracts_queryset(profile), pk=pk)

    if request.method == 'POST':
        form = OwnerContractUpdateForm(request.POST, instance=contract, owner_profile=profile)
        if form.is_valid():
            updated_contract = form.save(commit=False)
            updated_contract.room = contract.room
            updated_contract.tenant = contract.tenant
            try:
                updated_contract.save()
            except ValidationError as exc:
                form.add_error(None, exc)
            except IntegrityError:
                form.add_error('contract_code', 'This contract code is already in use.')
            else:
                messages.success(request, 'Contract updated successfully.')
                return redirect('portal:owner_contract_detail', pk=contract.pk)
    else:
        form = OwnerContractUpdateForm(instance=contract, owner_profile=profile)

    return render(request, 'portal/owner_contract_form.html', {
        'profile': profile,
        'contract': contract,
        'form': form,
        'form_title': 'Edit Contract',
        'submit_label': 'Save Changes',
    })


@owner_required
def owner_listings_list(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    listings = owner_listings_queryset(profile).order_by('-published_at', '-created_at')
    return render(request, 'portal/owner_listings_list.html', {
        'profile': profile,
        'listings': listings,
    })


@owner_required
def owner_listing_detail(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    listing = get_object_or_404(owner_listings_queryset(profile), pk=pk)
    return render(request, 'portal/owner_listing_detail.html', {
        'profile': profile,
        'listing': listing,
    })


@owner_required
def owner_listing_create(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    allowed_rooms = owner_rooms_queryset(profile).order_by('room_code')

    if request.method == 'POST':
        form = OwnerRoomListingForm(request.POST, allowed_rooms=allowed_rooms)
        if form.is_valid():
            try:
                form.save()
            except ValidationError as exc:
                form.add_error(None, exc)
            else:
                messages.success(request, 'Room listing created successfully.')
                return redirect('portal:owner_listings_list')
    else:
        form = OwnerRoomListingForm(allowed_rooms=allowed_rooms)

    return render(request, 'portal/owner_listing_form.html', {
        'profile': profile,
        'form': form,
        'form_title': 'Create Room Listing',
        'submit_label': 'Create Listing',
    })


@owner_required
def owner_listing_update(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    listing = get_object_or_404(owner_listings_queryset(profile), pk=pk)
    allowed_rooms = owner_rooms_queryset(profile).order_by('room_code')

    if request.method == 'POST':
        form = OwnerRoomListingForm(request.POST, instance=listing, allowed_rooms=allowed_rooms)
        if form.is_valid():
            try:
                form.save()
            except ValidationError as exc:
                form.add_error(None, exc)
            else:
                messages.success(request, 'Room listing updated successfully.')
                return redirect('portal:owner_listing_detail', pk=listing.pk)
    else:
        form = OwnerRoomListingForm(instance=listing, allowed_rooms=allowed_rooms)

    return render(request, 'portal/owner_listing_form.html', {
        'profile': profile,
        'listing': listing,
        'form': form,
        'form_title': 'Edit Room Listing',
        'submit_label': 'Save Changes',
    })


@owner_required
def owner_tenants_list(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    tenants = owner_tenants_queryset(profile).order_by('full_name')
    return render(request, 'portal/owner_tenants_list.html', {
        'profile': profile,
        'tenants': tenants,
    })


@owner_required
def owner_tenant_detail(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    tenant = get_object_or_404(owner_tenants_queryset(profile), pk=pk)
    contracts = owner_contracts_queryset(profile).filter(tenant=tenant).order_by('-start_date', 'contract_code')
    is_shared_tenant = is_tenant_shared_across_owners(tenant)
    return render(request, 'portal/owner_tenant_detail.html', {
        'profile': profile,
        'tenant': tenant,
        'contracts': contracts,
        'is_shared_tenant': is_shared_tenant,
    })


@owner_required
def owner_tenant_update(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    tenant = get_object_or_404(owner_tenants_queryset(profile), pk=pk)
    if is_tenant_shared_across_owners(tenant):
        messages.warning(
            request,
            'This tenant is linked to multiple owners, so their shared profile is read-only in the owner portal.',
        )
        return redirect('portal:owner_tenant_detail', pk=tenant.pk)

    if request.method == 'POST':
        form = OwnerTenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenant updated successfully.')
            return redirect('portal:owner_tenant_detail', pk=tenant.pk)
    else:
        form = OwnerTenantForm(instance=tenant)

    return render(request, 'portal/owner_tenant_form.html', {
        'profile': profile,
        'tenant': tenant,
        'form': form,
        'form_title': 'Edit Tenant',
        'submit_label': 'Save Changes',
    })


@owner_required
def owner_invoices_list(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    invoices = owner_invoices_queryset(profile).order_by('-year', '-month', 'invoice_code')
    return render(request, 'portal/owner_invoices_list.html', {
        'profile': profile,
        'invoices': invoices,
    })


@owner_required
def owner_invoice_detail(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    invoice = get_object_or_404(owner_invoices_queryset(profile), pk=pk)
    payments = owner_payments_queryset(profile).filter(invoice=invoice).order_by('-paid_at', '-created_at')
    return render(request, 'portal/owner_invoice_detail.html', {
        'profile': profile,
        'invoice': invoice,
        'payments': payments,
    })


@owner_required
def owner_invoice_create(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    if request.method == 'POST':
        form = OwnerInvoiceCreateForm(request.POST, owner_profile=profile)
        if form.is_valid():
            try:
                invoice = form.save()
            except ValidationError as exc:
                form.add_error(None, exc)
            except IntegrityError:
                form.add_error(None, 'An invoice already exists for this contract, month, and year.')
            else:
                messages.success(request, 'Invoice created successfully.')
                return redirect('portal:owner_invoice_detail', pk=invoice.pk)
    else:
        form = OwnerInvoiceCreateForm(owner_profile=profile)

    return render(request, 'portal/owner_invoice_form.html', {
        'profile': profile,
        'form': form,
        'form_title': 'Create Invoice',
        'submit_label': 'Create Invoice',
    })


@owner_required
def owner_invoice_update(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    invoice = get_object_or_404(owner_invoices_queryset(profile), pk=pk)

    if request.method == 'POST':
        original_contract = invoice.contract
        original_invoice_code = invoice.invoice_code
        original_total_amount = invoice.total_amount
        original_paid_amount = invoice.paid_amount
        original_remaining_amount = invoice.remaining_amount
        original_status = invoice.status

        form = OwnerInvoiceUpdateForm(request.POST, instance=invoice)
        if form.is_valid():
            updated_invoice = form.save(commit=False)
            updated_invoice.contract = original_contract
            updated_invoice.invoice_code = original_invoice_code
            updated_invoice.total_amount = original_total_amount
            updated_invoice.paid_amount = original_paid_amount
            updated_invoice.remaining_amount = original_remaining_amount
            updated_invoice.status = original_status
            try:
                updated_invoice.save()
            except ValidationError as exc:
                form.add_error(None, exc)
            except IntegrityError:
                form.add_error(None, 'An invoice already exists for this contract, month, and year.')
            else:
                messages.success(request, 'Invoice updated successfully.')
                return redirect('portal:owner_invoice_detail', pk=invoice.pk)
    else:
        form = OwnerInvoiceUpdateForm(instance=invoice)

    return render(request, 'portal/owner_invoice_form.html', {
        'profile': profile,
        'invoice': invoice,
        'form': form,
        'form_title': 'Edit Invoice',
        'submit_label': 'Save Changes',
    })


@owner_required
def owner_payment_create(request, invoice_pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    invoice = get_object_or_404(owner_invoices_queryset(profile), pk=invoice_pk)

    if request.method == 'POST':
        form = OwnerPaymentCreateForm(request.POST, invoice=invoice)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.collector = request.user
            try:
                payment.save()
            except ValidationError as exc:
                form.add_error(None, exc)
            else:
                messages.success(request, 'Payment recorded successfully.')
                return redirect('portal:owner_invoice_detail', pk=invoice.pk)
    else:
        form = OwnerPaymentCreateForm(invoice=invoice)

    return render(request, 'portal/owner_payment_form.html', {
        'profile': profile,
        'invoice': invoice,
        'form': form,
    })


@owner_required
def owner_repairs_list(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    repairs = owner_repairs_queryset(profile).order_by('-requested_at', '-created_at')
    return render(request, 'portal/owner_repairs_list.html', {
        'profile': profile,
        'repairs': repairs,
    })


@owner_required
def owner_repair_detail(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    repair = get_object_or_404(owner_repairs_queryset(profile), pk=pk)
    return render(request, 'portal/owner_repair_detail.html', {
        'profile': profile,
        'repair': repair,
    })


@owner_required
def owner_repair_process(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    repair = get_object_or_404(owner_repairs_queryset(profile), pk=pk)

    if request.method == 'POST':
        form = OwnerRepairProcessForm(request.POST, instance=repair)
        if form.is_valid():
            form.save()
            messages.success(request, 'Repair request updated successfully.')
            return redirect('portal:owner_repairs_list')
    else:
        form = OwnerRepairProcessForm(instance=repair)

    return render(request, 'portal/owner_repair_process_form.html', {
        'profile': profile,
        'repair': repair,
        'form': form,
    })


@owner_required
def owner_viewing_registrations_list(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    registrations = owner_viewing_registrations_queryset(profile).order_by('-created_at')
    return render(request, 'portal/owner_viewing_registrations_list.html', {
        'profile': profile,
        'registrations': registrations,
    })


@owner_required
def owner_viewing_registration_detail(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    registration = get_object_or_404(owner_viewing_registrations_queryset(profile), pk=pk)
    return render(request, 'portal/owner_viewing_registration_detail.html', {
        'profile': profile,
        'registration': registration,
    })


@owner_required
def owner_viewing_registration_process(request, pk):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    registration = get_object_or_404(owner_viewing_registrations_queryset(profile), pk=pk)

    if request.method == 'POST':
        form = OwnerViewingRegistrationProcessForm(request.POST)
        if form.is_valid():
            owner_viewing_registrations_queryset(profile).filter(pk=registration.pk).update(
                status=form.cleaned_data['status'],
                admin_note=form.cleaned_data['admin_note'],
                updated_at=timezone.now(),
            )
            messages.success(request, 'Viewing registration updated successfully.')
            return redirect('portal:owner_viewing_registrations_list')
    else:
        form = OwnerViewingRegistrationProcessForm(initial={
            'status': registration.status,
            'admin_note': registration.admin_note,
        })

    return render(request, 'portal/owner_viewing_registration_process_form.html', {
        'profile': profile,
        'registration': registration,
        'form': form,
    })


@tenant_required
def tenant_dashboard(request):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    active_contract_status = _choice_value(Contract.STATUS_CHOICES, 'Active', 'active')
    open_repair_statuses = [
        RepairRequest.STATUS_PENDING,
        RepairRequest.STATUS_IN_PROGRESS,
    ]

    active_contract = (
        Contract.objects
        .select_related('room')
        .filter(tenant=tenant, status=active_contract_status)
        .order_by('-start_date')
        .first()
    )
    invoices = Invoice.objects.filter(contract__tenant=tenant)
    open_repairs = RepairRequest.objects.filter(tenant=tenant, status__in=open_repair_statuses)
    unread_notifications = Notification.objects.filter(tenant=tenant, is_read=False)
    invoices_needing_payment = invoices.filter(
        status__in=[Invoice.STATUS_UNPAID, Invoice.STATUS_PARTIAL, Invoice.STATUS_OVERDUE],
    )

    metrics = {
        'tenant_name': tenant.full_name,
        'current_contract': active_contract,
        'unpaid_or_partial_invoices': invoices_needing_payment.count(),
        'outstanding_balance': _money_sum(invoices_needing_payment, 'remaining_amount'),
        'open_repair_requests': open_repairs.count(),
        'unread_notifications': unread_notifications.count(),
    }

    recent = {
        'invoices': invoices.order_by('-year', '-month', '-created_at')[:5],
        'repairs': RepairRequest.objects.filter(tenant=tenant).order_by('-requested_at', '-created_at')[:4],
        'notifications': Notification.objects.filter(tenant=tenant).order_by('-created_at')[:4],
    }

    return render(request, 'portal/tenant_dashboard.html', {
        'tenant': tenant,
        'metrics': metrics,
        'recent': recent,
    })


@tenant_required
def tenant_profile(request):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    return render(request, 'portal/tenant_profile.html', {
        'tenant': tenant,
    })


@tenant_required
def tenant_contracts_list(request):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    contracts = tenant_contracts_queryset(tenant).order_by('-start_date', 'contract_code')
    return render(request, 'portal/tenant_contracts_list.html', {
        'tenant': tenant,
        'contracts': contracts,
    })


@tenant_required
def tenant_contract_detail(request, pk):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    contract = get_object_or_404(tenant_contracts_queryset(tenant), pk=pk)
    return render(request, 'portal/tenant_contract_detail.html', {
        'tenant': tenant,
        'contract': contract,
    })


@tenant_required
def tenant_invoices_list(request):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    invoices = tenant_invoices_queryset(tenant).order_by('-year', '-month', 'invoice_code')
    return render(request, 'portal/tenant_invoices_list.html', {
        'tenant': tenant,
        'invoices': invoices,
    })


@tenant_required
def tenant_invoice_detail(request, pk):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    invoice = get_object_or_404(tenant_invoices_queryset(tenant), pk=pk)
    return render(request, 'portal/tenant_invoice_detail.html', {
        'tenant': tenant,
        'invoice': invoice,
    })


@tenant_required
def tenant_payments_list(request):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    payments = tenant_payments_queryset(tenant).order_by('-paid_at', '-created_at')
    return render(request, 'portal/tenant_payments_list.html', {
        'tenant': tenant,
        'payments': payments,
    })


@tenant_required
def tenant_repairs_list(request):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    repairs = tenant_repairs_queryset(tenant).order_by('-requested_at', '-created_at')
    return render(request, 'portal/tenant_repairs_list.html', {
        'tenant': tenant,
        'repairs': repairs,
    })


@tenant_required
def tenant_repair_create(request):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    allowed_rooms = tenant_active_rooms_queryset(tenant)
    has_allowed_rooms = allowed_rooms.exists()

    if request.method == 'POST':
        form = TenantRepairRequestForm(request.POST, allowed_rooms=allowed_rooms)
        if not has_allowed_rooms:
            messages.error(request, 'No active room is linked to your tenant profile.')
        elif form.is_valid():
            repair = form.save(commit=False)
            repair.tenant = tenant
            repair.save()
            messages.success(request, 'Repair request submitted successfully.')
            return redirect('portal:tenant_repairs_list')
    else:
        form = TenantRepairRequestForm(allowed_rooms=allowed_rooms)

    return render(request, 'portal/tenant_repair_form.html', {
        'tenant': tenant,
        'form': form,
        'has_allowed_rooms': has_allowed_rooms,
    })


@tenant_required
def tenant_repair_detail(request, pk):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    repair = get_object_or_404(tenant_repairs_queryset(tenant), pk=pk)
    return render(request, 'portal/tenant_repair_detail.html', {
        'tenant': tenant,
        'repair': repair,
    })


@tenant_required
def tenant_notifications_list(request):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    notifications = tenant_notifications_queryset(tenant).order_by('-created_at')
    return render(request, 'portal/tenant_notifications_list.html', {
        'tenant': tenant,
        'notifications': notifications,
    })


@tenant_required
def tenant_notification_detail(request, pk):
    tenant = get_tenant_profile(request.user)
    if not tenant:
        return render_missing_tenant_profile(request)

    notification = get_object_or_404(tenant_notifications_queryset(tenant), pk=pk)
    return render(request, 'portal/tenant_notification_detail.html', {
        'tenant': tenant,
        'notification': notification,
    })


def access_denied(request):
    return render(request, 'portal/access_denied.html', status=403)
