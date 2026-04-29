from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from orders.models import Invoice, Order, OrderItem, PaymentTransaction, ShippingMethod, ShippingZone


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["line_total"]



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "full_name", "status", "payment_status", "total", "created_at", "map_link", "print_invoice"]
    list_filter = ["status", "payment_status", "payment_method"]
    search_fields = ["order_number", "email", "full_name", "phone"]
    inlines = [OrderItemInline]
    readonly_fields = ["map_link"]

    def map_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://maps.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank">Open Map</a>', url)
        return "-"
    map_link.short_description = "Location Map"

    def print_invoice(self, obj):
        url = reverse('orders:invoice', args=[obj.order_number])
        return format_html('<a class="button" href="{}" target="_blank">Print</a>', url)
    print_invoice.short_description = 'Invoice'


admin.site.register(ShippingZone)
admin.site.register(ShippingMethod)
admin.site.register(PaymentTransaction)
admin.site.register(Invoice)
