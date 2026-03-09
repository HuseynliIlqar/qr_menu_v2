from django.urls import path
from qr_menu_app.views.index_view import index_page


urlpatterns = [
    path("", index_page, name="index"),
]
