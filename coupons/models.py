from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", _("Percentage")
        FIXED = "fixed", _("Fixed amount")

    code = models.CharField(max_length=40, unique=True)
    discount_type = models.CharField(max_length=12, choices=DiscountType.choices, default=DiscountType.PERCENT)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField(blank=True, null=True)
    usage_limit = models.PositiveIntegerField(default=0, help_text=_("0 means unlimited"))
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid_for(self, amount):
        now = timezone.now()
        if not self.is_active or amount < self.min_order_amount:
            return False
        if self.end_at and self.end_at < now:
            return False
        return not self.usage_limit or self.used_count < self.usage_limit

    def discount_for(self, amount):
        if not self.is_valid_for(amount):
            return Decimal("0.00")
        if self.discount_type == self.DiscountType.PERCENT:
            return min(amount, amount * (self.value / Decimal("100")))
        return min(amount, self.value)
