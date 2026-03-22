from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# Tenant-specific URLs (each restaurant subdomain)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('qr_menu_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
