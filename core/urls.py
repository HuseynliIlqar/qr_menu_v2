from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from calls.views import service_worker_view


# Tenant-specific URLs (each restaurant subdomain)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    # Service worker must live at the root scope for push notifications
    path('sw.js', service_worker_view, name='service_worker'),
    path('', include('calls.urls')),
    path('', include('qr_menu_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
