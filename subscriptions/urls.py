from django.urls import path

from subscriptions import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.pricing, name="pricing"),
    path("subscribe/<slug:plan_code>/", views.subscribe, name="subscribe"),
    path("payment/<int:subscription_id>/", views.payment, name="payment"),
    path("my-store/", views.my_store, name="my_store"),
]
