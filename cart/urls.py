from django.urls import path

from cart import views

app_name = "cart"

urlpatterns = [
    path("", views.detail, name="detail"),
    path("add/<int:product_id>/", views.add, name="add"),
    path("update/<int:item_id>/", views.update, name="update"),
    path("remove/<int:item_id>/", views.remove, name="remove"),
    path("coupon/", views.apply_coupon, name="apply_coupon"),
]
