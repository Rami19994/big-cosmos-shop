from decimal import Decimal
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ShippingZone(models.Model):
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=80)
    city = models.CharField(max_length=80, blank=True)
    region = models.CharField(max_length=80, blank=True)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_days = models.CharField(max_length=80, default="2-5 days")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ShippingMethod(models.Model):
    class Type(models.TextChoices):
        DELIVERY = "delivery", _("Delivery")
        LOCAL = "local", _("Local delivery")
        PICKUP = "pickup", _("Pickup from store")

    name_en = models.CharField(max_length=120)
    name_ar = models.CharField(max_length=120, blank=True)
    method_type = models.CharField(max_length=20, choices=Type.choices, default=Type.DELIVERY)
    base_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_days = models.CharField(max_length=80, default="2-5 days")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name_en


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        PROCESSING = "processing", _("Processing")
        SHIPPED = "shipped", _("Shipped")
        DELIVERED = "delivered", _("Delivered")
        CANCELLED = "cancelled", _("Cancelled")
        REFUNDED = "refunded", _("Refunded")

    class PaymentStatus(models.TextChoices):
        UNPAID = "unpaid", _("Unpaid")
        PAID = "paid", _("Paid")
        FAILED = "failed", _("Failed")
        REFUNDED = "refunded", _("Refunded")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="orders", blank=True, null=True)
    order_number = models.CharField(max_length=30, unique=True, blank=True)
    email = models.EmailField()
    full_name = models.CharField(max_length=140)
    phone = models.CharField(max_length=40)
    country = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    region = models.CharField(max_length=80, blank=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=40, default="cod")
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_reference = models.CharField(max_length=120, blank=True)
    shipping_method = models.CharField(max_length=120, blank=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    coupon_code = models.CharField(max_length=40, blank=True)
    tracking_number = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"NC-{uuid.uuid4().hex[:10].upper()}"
        self.total = (self.subtotal + self.shipping_fee + self.tax_total) - self.discount_total
        if self.total < 0:
            self.total = Decimal("0.00")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={"order_number": self.order_number})

    @property
    def can_cancel(self):
        return self.status in {self.Status.PENDING, self.Status.PROCESSING}


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, blank=True, null=True)
    product_name = models.CharField(max_length=180)
    sku = models.CharField(max_length=80)
    variant_label = models.CharField(max_length=160, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class PaymentTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="transactions")
    provider = models.CharField(max_length=40, default="manual")
    reference = models.CharField(max_length=120, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")
    raw_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoice")
    invoice_number = models.CharField(max_length=30, unique=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{self.order.order_number}"
        super().save(*args, **kwargs)
