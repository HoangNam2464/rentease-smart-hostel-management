from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from billing.models import Invoice, PaymentHistory
from contracts.models import Contract
from listings.models import RoomListing, ViewingRegistration
from maintenance.models import Notification, RepairRequest
from properties.models import Room
from tenants.models import Tenant

from .decorators import is_admin_user, owner_required, tenant_required
from .forms import OwnerRepairProcessForm, RentEaseAuthenticationForm, TenantRepairRequestForm


def _choice_value(choices, label, fallback):
    for value, display in choices:
        if display == label:
            return value
    return fallback


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
    return Room.objects.filter(owner=profile)


def owner_contracts_queryset(profile):
    return Contract.objects.select_related('room', 'tenant').filter(room__owner=profile)


def owner_listings_queryset(profile):
    return RoomListing.objects.select_related('room').filter(room__owner=profile)


def owner_tenants_queryset(profile):
    return Tenant.objects.filter(contracts__room__owner=profile).distinct()


def owner_invoices_queryset(profile):
    return (
        Invoice.objects
        .select_related('contract', 'contract__room', 'contract__tenant')
        .filter(contract__room__owner=profile)
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
    messages.success(request, 'You have been logged out.')
    return redirect('/')


@login_required(login_url='/login/')
def dashboard_redirect(request):
    return redirect(get_role_redirect_url(request.user))


@owner_required
def owner_dashboard(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    occupied_status = _choice_value(Room.STATUS_CHOICES, 'Occupied', 'occupied')
    active_contract_status = _choice_value(Contract.STATUS_CHOICES, 'Active', 'active')

    owner_rooms = owner_rooms_queryset(profile)
    owner_contracts = owner_contracts_queryset(profile)
    owner_invoices = Invoice.objects.filter(contract__room__owner=profile)

    metrics = {
        'total_rooms': owner_rooms.count(),
        'occupied_rooms': owner_rooms.filter(status=occupied_status).count(),
        'active_contracts': owner_contracts.filter(status=active_contract_status).count(),
        'unpaid_or_partial_invoices': owner_invoices.filter(
            status__in=[Invoice.STATUS_UNPAID, Invoice.STATUS_PARTIAL],
        ).count(),
        'pending_repair_requests': RepairRequest.objects.filter(
            room__owner=profile,
            status=RepairRequest.STATUS_PENDING,
        ).count(),
        'published_listings': RoomListing.objects.filter(
            room__owner=profile,
            status=RoomListing.STATUS_PUBLISHED,
        ).count(),
    }

    return render(request, 'portal/owner_dashboard.html', {
        'profile': profile,
        'metrics': metrics,
    })


@owner_required
def owner_rooms_list(request):
    profile = get_owner_profile(request.user)
    if not profile:
        return render_missing_owner_profile(request)

    rooms = owner_rooms_queryset(profile).order_by('room_code')
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
    return render(request, 'portal/owner_tenant_detail.html', {
        'profile': profile,
        'tenant': tenant,
        'contracts': contracts,
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
    return render(request, 'portal/owner_invoice_detail.html', {
        'profile': profile,
        'invoice': invoice,
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

    metrics = {
        'tenant_name': tenant.full_name,
        'current_contract': active_contract,
        'unpaid_or_partial_invoices': invoices.filter(
            status__in=[Invoice.STATUS_UNPAID, Invoice.STATUS_PARTIAL],
        ).count(),
        'open_repair_requests': open_repairs.count(),
        'unread_notifications': unread_notifications.count(),
    }

    return render(request, 'portal/tenant_dashboard.html', {
        'tenant': tenant,
        'metrics': metrics,
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
