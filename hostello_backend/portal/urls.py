from django.urls import path

from . import views


app_name = 'portal'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/rooms/', views.owner_rooms_list, name='owner_rooms_list'),
    path('owner/rooms/<int:pk>/', views.owner_room_detail, name='owner_room_detail'),
    path('owner/tenants/', views.owner_tenants_list, name='owner_tenants_list'),
    path('owner/tenants/<int:pk>/', views.owner_tenant_detail, name='owner_tenant_detail'),
    path('owner/contracts/', views.owner_contracts_list, name='owner_contracts_list'),
    path('owner/contracts/<int:pk>/', views.owner_contract_detail, name='owner_contract_detail'),
    path('owner/invoices/', views.owner_invoices_list, name='owner_invoices_list'),
    path('owner/invoices/<int:pk>/', views.owner_invoice_detail, name='owner_invoice_detail'),
    path('owner/repairs/', views.owner_repairs_list, name='owner_repairs_list'),
    path('owner/repairs/<int:pk>/', views.owner_repair_detail, name='owner_repair_detail'),
    path('owner/listings/', views.owner_listings_list, name='owner_listings_list'),
    path('owner/listings/<int:pk>/', views.owner_listing_detail, name='owner_listing_detail'),
    path('owner/viewing-registrations/', views.owner_viewing_registrations_list, name='owner_viewing_registrations_list'),
    path('owner/viewing-registrations/<int:pk>/', views.owner_viewing_registration_detail, name='owner_viewing_registration_detail'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('tenant/profile/', views.tenant_profile, name='tenant_profile'),
    path('tenant/contracts/', views.tenant_contracts_list, name='tenant_contracts_list'),
    path('tenant/contracts/<int:pk>/', views.tenant_contract_detail, name='tenant_contract_detail'),
    path('tenant/invoices/', views.tenant_invoices_list, name='tenant_invoices_list'),
    path('tenant/invoices/<int:pk>/', views.tenant_invoice_detail, name='tenant_invoice_detail'),
    path('tenant/payments/', views.tenant_payments_list, name='tenant_payments_list'),
    path('tenant/repairs/', views.tenant_repairs_list, name='tenant_repairs_list'),
    path('tenant/repairs/new/', views.tenant_repair_create, name='tenant_repair_create'),
    path('tenant/repairs/<int:pk>/', views.tenant_repair_detail, name='tenant_repair_detail'),
    path('tenant/notifications/', views.tenant_notifications_list, name='tenant_notifications_list'),
    path('tenant/notifications/<int:pk>/', views.tenant_notification_detail, name='tenant_notification_detail'),
    path('access-denied/', views.access_denied, name='access_denied'),
]
