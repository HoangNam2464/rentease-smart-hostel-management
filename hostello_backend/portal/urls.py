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
    path('owner/contracts/', views.owner_contracts_list, name='owner_contracts_list'),
    path('owner/contracts/<int:pk>/', views.owner_contract_detail, name='owner_contract_detail'),
    path('owner/listings/', views.owner_listings_list, name='owner_listings_list'),
    path('owner/listings/<int:pk>/', views.owner_listing_detail, name='owner_listing_detail'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('access-denied/', views.access_denied, name='access_denied'),
]
