from django.contrib import admin
from coupons.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "discount_type", "value", "is_active", "used_count"]
    list_filter = ["discount_type", "is_active"]
    search_fields = ["code"]
