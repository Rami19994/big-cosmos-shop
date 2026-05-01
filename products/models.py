from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils import translation
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    logo = models.ImageField(upload_to="brands/", blank=True)
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    class Availability(models.TextChoices):
        IN_STOCK = "in_stock", _("In stock")
        OUT_OF_STOCK = "out_of_stock", _("Out of stock")
        PREORDER = "preorder", _("Pre-order")

    category = models.ForeignKey("categories.Category", on_delete=models.PROTECT, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name="products", blank=True, null=True)
    name_en = models.CharField(max_length=180)
    name_ar = models.CharField(max_length=180, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    sku = models.CharField(max_length=80, unique=True)
    summary_en = models.CharField(max_length=255, blank=True)
    summary_ar = models.CharField(max_length=255, blank=True)
    description_en = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=8, default="USD")
    stock_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    availability = models.CharField(max_length=20, choices=Availability.choices, default=Availability.IN_STOCK)
    tags = models.CharField(max_length=255, blank=True, help_text=_("Comma-separated tags"))
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to="products/videos/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_hot = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    related_products = models.ManyToManyField("self", blank=True)
    upsell_products = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="upsold_by")
    cross_sell_products = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="cross_sold_by")
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["sku"]), models.Index(fields=["is_active"])]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en) or self.sku.lower()
        if self.stock_quantity <= 0:
            self.availability = self.Availability.OUT_OF_STOCK
        super().save(*args, **kwargs)

    @property
    def name(self):
        return self.name_ar if translation.get_language() == "ar" and self.name_ar else self.name_en

    @property
    def summary(self):
        return self.summary_ar if translation.get_language() == "ar" and self.summary_ar else self.summary_en

    @property
    def description(self):
        return self.description_ar if translation.get_language() == "ar" and self.description_ar else self.description_en

    @property
    def current_price(self):
        return self.discount_price or self.price

    @property
    def discount_percent(self):
        if self.discount_price and self.price:
            return int((Decimal("1") - (self.discount_price / self.price)) * 100)
        return 0

    @property
    def rating_average(self):
        return self.reviews.filter(is_approved=True).aggregate(avg=Avg("rating"))["avg"] or 0

    @property
    def low_stock(self):
        return 0 < self.stock_quantity <= self.low_stock_threshold

    @property
    def images_360(self):
        return self.images.filter(is_360_view=True)

    def get_absolute_url(self):

        return reverse("products:detail", kwargs={"slug": self.slug})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    alt_text = models.CharField(max_length=160, blank=True)
    is_main = models.BooleanField(default=False)
    is_360_view = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.alt_text or self.product.name_en

    @property
    def url(self):
        try:
            return self.image.url if self.image else ""
        except (ValueError, AttributeError):
            return ""


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    name_en = models.CharField(max_length=80)
    name_ar = models.CharField(max_length=80, blank=True)
    value = models.CharField(max_length=120)
    sku = models.CharField(max_length=80, unique=True)
    price_delta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name_en} - {self.name}: {self.value}"

    @property
    def name(self):
        return self.name_ar if translation.get_language() == "ar" and self.name_ar else self.name_en


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    name_en = models.CharField(max_length=120)
    name_ar = models.CharField(max_length=120, blank=True)
    value_en = models.CharField(max_length=255)
    value_ar = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    @property
    def name(self):
        return self.name_ar if translation.get_language() == "ar" and self.name_ar else self.name_en

    @property
    def value(self):
        return self.value_ar if translation.get_language() == "ar" and self.value_ar else self.value_en


class ProductQuestion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="questions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=120, blank=True)
    question = models.TextField()
    answer = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class StockMovement(models.Model):
    class Type(models.TextChoices):
        IN = "in", _("Stock in")
        OUT = "out", _("Stock out")
        ADJUST = "adjust", _("Manual adjustment")

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_movements")
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, blank=True, null=True)
    movement_type = models.CharField(max_length=12, choices=Type.choices)
    quantity = models.IntegerField()
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
