from decimal import Decimal

from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carts", blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    coupon = models.ForeignKey("coupons.Coupon", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.pk or 'new'}"

    @property
    def subtotal(self):
        return sum((item.line_total for item in self.items.select_related("product", "variant")), Decimal("0.00"))

    @property
    def discount_total(self):
        return self.coupon.discount_for(self.subtotal) if self.coupon else Decimal("0.00")

    @property
    def total(self):
        return max(self.subtotal - self.discount_total, Decimal("0.00"))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    variant = models.ForeignKey("products.ProductVariant", on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["cart", "product", "variant"]]

    @property
    def unit_price(self):
        return self.product.current_price + (self.variant.price_delta if self.variant else Decimal("0.00"))

    @property
    def line_total(self):
        return self.unit_price * self.quantity
