from django.urls import path

from . import views


app_name = 'portal'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('access-denied/', views.access_denied, name='access_denied'),
]
