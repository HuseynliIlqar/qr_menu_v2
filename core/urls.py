from django.contrib import admin
from django.urls import path, include
from django_tenants.utils import get_public_schema_name, schema_context


# Tenant-specific URLs (each restaurant subdomain)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('qr_menu_app.urls')),
]
