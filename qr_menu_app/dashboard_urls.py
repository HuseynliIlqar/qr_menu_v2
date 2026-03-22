from django.urls import path
from django.contrib.auth.views import LogoutView

from qr_menu_app.views.dashboard import (
    TenantLoginView,
    auto_login,
    dashboard_home,
    edit_restaurant,
    edit_sliders,
    edit_social,
    edit_info,
    edit_gallery,
    edit_categories,
    menu_list,
    menu_add,
    menu_edit,
    menu_delete,
)

app_name = 'dashboard'

urlpatterns = [
    path('login/', TenantLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/dashboard/login/'), name='logout'),
    path('auto-login/', auto_login, name='auto_login'),
    path('', dashboard_home, name='home'),
    path('restaurant/', edit_restaurant, name='restaurant'),
    path('sliders/', edit_sliders, name='sliders'),
    path('social/', edit_social, name='social'),
    path('info/', edit_info, name='info'),
    path('gallery/', edit_gallery, name='gallery'),
    path('categories/', edit_categories, name='categories'),
    path('menu/', menu_list, name='menu_list'),
    path('menu/add/', menu_add, name='menu_add'),
    path('menu/<int:pk>/', menu_edit, name='menu_edit'),
    path('menu/<int:pk>/delete/', menu_delete, name='menu_delete'),
]
