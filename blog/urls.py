from django.urls import path

from blog import views
app_name = "blog"

urlpatterns = [path("", views.listing, name="list"), path("<slug:slug>/", views.detail, name="detail")]
