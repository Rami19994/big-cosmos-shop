from django.urls import path

from products import views
app_name = "products"

urlpatterns = [
    path("", views.listing, name="list"),
    path("search/", views.search, name="search"),
    path("suggestions/", views.suggestions, name="suggestions"),
    path("compare/", views.compare, name="compare"),
    path("compare/add/<int:product_id>/", views.compare_add, name="compare_add"),
    path("category/<slug:slug>/", views.category, name="category"),
    path("<slug:slug>/", views.detail, name="detail"),
    path("wishlist/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),
]
