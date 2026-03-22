from django.urls import path, include
from qr_menu_app.views.index_view import index_page


urlpatterns = [
    path("", index_page, name="index"),
    path("dashboard/", include("qr_menu_app.dashboard_urls")),
]
