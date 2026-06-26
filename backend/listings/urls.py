from django.urls import path

from . import views


app_name = 'listings'

urlpatterns = [
    path('', views.public_listing_list, name='public_listing_list'),
    path('<int:pk>/', views.public_listing_detail, name='public_listing_detail'),
    path('<int:pk>/register/', views.viewing_registration_create, name='viewing_registration_create'),
    path('<int:pk>/register/success/', views.viewing_registration_success, name='viewing_registration_success'),
]
