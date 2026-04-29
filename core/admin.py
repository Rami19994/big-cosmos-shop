from django.contrib import admin
from core.models import StoreSetting


@admin.register(StoreSetting)
class StoreSettingAdmin(admin.ModelAdmin):
    list_display = ["site_name", "currency", "email", "phone", "updated_at"]
