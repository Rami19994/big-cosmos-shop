from django.urls import path

from core import views
app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="home"),
    path("products/", views.manage_products, name="products"),
    path("orders/", views.manage_orders, name="orders"),
    path("customers/", views.manage_customers, name="customers"),
    path("inventory/", views.inventory, name="inventory"),
    path("reports/", views.reports, name="reports"),
    path("settings/", views.settings, name="settings"),
    path("exports/orders/", views.export_orders, name="export_orders"),
]
