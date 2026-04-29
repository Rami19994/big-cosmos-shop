from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("confirmation/<str:order_number>/", views.confirmation, name="confirmation"),
    path("history/", views.history, name="history"),
    path("<str:order_number>/", views.detail, name="detail"),
    path("<str:order_number>/cancel/", views.cancel, name="cancel"),
    path("<str:order_number>/invoice/", views.invoice, name="invoice"),
]
