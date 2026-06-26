from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from . import services


@staff_member_required(login_url='admin:login')
def dashboard(request):
    return render(request, 'reports/dashboard.html', {
        'title': 'RentEase Reports',
        'metrics': services.dashboard_metrics(),
    })


@staff_member_required(login_url='admin:login')
def billing_report(request):
    context = services.billing_report(
        month=request.GET.get('month'),
        year=request.GET.get('year'),
        status=request.GET.get('status'),
    )
    context['title'] = 'Billing Report'
    return render(request, 'reports/billing_report.html', context)


@staff_member_required(login_url='admin:login')
def room_report(request):
    context = services.room_report()
    context['title'] = 'Room Report'
    return render(request, 'reports/room_report.html', context)


@staff_member_required(login_url='admin:login')
def tenant_contract_report(request):
    context = services.tenant_contract_report()
    context['title'] = 'Tenant and Contract Report'
    return render(request, 'reports/tenant_contract_report.html', context)


@staff_member_required(login_url='admin:login')
def maintenance_report(request):
    context = services.maintenance_report()
    context['title'] = 'Maintenance Report'
    return render(request, 'reports/maintenance_report.html', context)


@staff_member_required(login_url='admin:login')
def listing_report(request):
    context = services.listing_report()
    context['title'] = 'Listing and Viewing Report'
    return render(request, 'reports/listing_report.html', context)
