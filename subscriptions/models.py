from decimal import Decimal
from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import get_language, gettext_lazy as _


class SubscriptionPlan(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=80)
    name_ar = models.CharField(max_length=80, blank=True)
    tagline = models.CharField(max_length=160)
    tagline_ar = models.CharField(max_length=160, blank=True)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2)
    annual_price = models.DecimalField(max_digits=8, decimal_places=2)
    product_limit = models.PositiveIntegerField(default=0, help_text="Zero means unlimited products.")
    features = models.JSONField(default=list, blank=True)
    features_ar = models.JSONField(default=list, blank=True)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "monthly_price"]

    def __str__(self):
        return self.name

    def price_for(self, billing_cycle):
        return self.annual_price if billing_cycle == StoreSubscription.BillingCycle.ANNUAL else self.monthly_price

    @property
    def display_name(self):
        return self.name_ar if get_language() == "ar" and self.name_ar else self.name

    @property
    def display_tagline(self):
        return self.tagline_ar if get_language() == "ar" and self.tagline_ar else self.tagline

    @property
    def display_features(self):
        return self.features_ar if get_language() == "ar" and self.features_ar else self.features


class Store(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="store")
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "store"
            slug = base_slug
            suffix = 2
            while Store.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def active_subscription(self):
        return self.subscriptions.filter(
            status=StoreSubscription.Status.ACTIVE,
            current_period_end__gte=timezone.now(),
        ).order_by("-current_period_end").first()


class StoreSubscription(models.Model):
    class BillingCycle(models.TextChoices):
        MONTHLY = "monthly", _("Monthly")
        ANNUAL = "annual", _("Annual")

    class Status(models.TextChoices):
        PENDING = "pending", _("Pending payment")
        ACTIVE = "active", _("Active")
        EXPIRED = "expired", _("Expired")
        CANCELLED = "cancelled", _("Cancelled")

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name="subscriptions")
    billing_cycle = models.CharField(max_length=12, choices=BillingCycle.choices)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    current_period_start = models.DateTimeField(blank=True, null=True)
    current_period_end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.store} — {self.plan}"

    def activate(self):
        now = timezone.now()
        self.status = self.Status.ACTIVE
        self.current_period_start = now
        self.current_period_end = now + timedelta(days=365 if self.billing_cycle == self.BillingCycle.ANNUAL else 30)
        self.save(update_fields=["status", "current_period_start", "current_period_end"])


class SubscriptionPayment(models.Model):
    class Method(models.TextChoices):
        BANK = "bank", _("Bank transfer")
        STRIPE = "stripe", "Stripe"
        PAYPAL = "paypal", "PayPal"

    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        FAILED = "failed", _("Failed")

    subscription = models.ForeignKey(StoreSubscription, on_delete=models.CASCADE, related_name="payments")
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    reference = models.CharField(max_length=32, unique=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"SUB-{uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)
