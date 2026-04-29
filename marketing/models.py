from django.db import models
from django.utils import timezone, translation


class Banner(models.Model):
    title_en = models.CharField(max_length=160)
    title_ar = models.CharField(max_length=160, blank=True)
    subtitle_en = models.CharField(max_length=255, blank=True)
    subtitle_ar = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="banners/", blank=True)
    link = models.URLField(blank=True)
    placement = models.CharField(max_length=40, default="home")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    @property
    def title(self):
        return self.title_ar if translation.get_language() == "ar" and self.title_ar else self.title_en

    @property
    def subtitle(self):
        return self.subtitle_ar if translation.get_language() == "ar" and self.subtitle_ar else self.subtitle_en


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    quote_en = models.TextField()
    quote_ar = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)

    @property
    def quote(self):
        return self.quote_ar if translation.get_language() == "ar" and self.quote_ar else self.quote_en


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class FlashSale(models.Model):
    title = models.CharField(max_length=160)
    products = models.ManyToManyField("products.Product", blank=True)
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    @property
    def live(self):
        now = timezone.now()
        return self.is_active and self.starts_at <= now <= self.ends_at
