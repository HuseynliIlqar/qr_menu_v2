from django.urls import path

from . import views

app_name = 'calls'

urlpatterns = [
    # Cashier
    path('cashier/generate/', views.generate_view, name='generate'),

    # Customer-facing
    path('customer/wait/<str:token>/', views.wait_view, name='wait'),
    path('customer/subscribe/<str:token>/', views.subscribe_view, name='subscribe'),

    # Barman dashboard
    path('bar/dashboard/', views.dashboard_view, name='dashboard'),
    path('bar/dashboard/data/', views.dashboard_data_view, name='dashboard_data'),
    path('bar/call/<str:token>/', views.call_customer_view, name='call'),
    path('bar/update-name/<str:token>/', views.update_name_view, name='update_name'),
    path('bar/done/<str:token>/', views.mark_done_view, name='done'),
]
