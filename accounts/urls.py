from django.urls import path
from django.views.generic import TemplateView

from accounts import views
app_name = "accounts"

urlpatterns = [
    path("login/", views.StoreLoginView.as_view(), name="login"),
    path("logout/", views.StoreLogoutView.as_view(), name="logout"),
    path("register/", TemplateView.as_view(template_name="accounts/register.html"), name="register"),
    path("profile/", views.profile, name="profile"),
    path("addresses/", views.addresses, name="addresses"),
    path("addresses/<int:pk>/delete/", views.delete_address, name="delete_address"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("settings/", views.settings, name="settings"),
    path("password-reset/", views.password_reset, name="password_reset"),
    path("password-reset/done/", views.password_reset_done, name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("password-reset/complete/", views.password_reset_complete, name="password_reset_complete"),
]
