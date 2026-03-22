from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from public import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.landing, name='public_landing'),
    path('register/', views.register_view, name='public_register'),
    path('login/', views.login_view, name='public_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
