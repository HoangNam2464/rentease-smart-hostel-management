from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from listings.views import home_page_view

urlpatterns = [
    path('', home_page_view, name='home'),
    path('admin/', admin.site.urls),
    path("rooms/", include("listings.urls")),
    path("api/billing/", include("billing.api.urls")),
    path('', include('portal.urls')),
    path("reports/", include("reports.urls")),
    path("accounts/login/", RedirectView.as_view(url="/login/", permanent=False))
]

if getattr(settings, 'INCLUDE_LEGACY_APPS', False):
    from fees import admin as fees_admin 
    urlpatterns += [
        path('legacy/', include('students.urls')),
    ]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
