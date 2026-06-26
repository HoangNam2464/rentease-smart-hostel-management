from django.urls import path

from . import views


app_name = 'reports'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('billing/', views.billing_report, name='billing'),
    path('rooms/', views.room_report, name='rooms'),
    path('tenants-contracts/', views.tenant_contract_report, name='tenants_contracts'),
    path('maintenance/', views.maintenance_report, name='maintenance'),
    path('listings/', views.listing_report, name='listings'),
]
