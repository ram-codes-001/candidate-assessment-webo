"""
CTMS root URL configuration.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root → login
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # Authentication
    path('', include('accounts.urls')),

    # Dashboard
    path('dashboard/', include('ctms.dashboard_urls')),

    # Clinical data modules
    path('patients/', include('patients.urls')),
    path('visits/', include('visits.urls')),
    path('labs/', include('labs.urls')),
    path('adverse-events/', include('adverse_events.urls')),

    # Reports & Export
    path('reports/', include('reports.urls')),

    # Audit Trail
    path('audit/', include('audit.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
