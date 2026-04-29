from django.db import models
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="children", blank=True, null=True)
    name_en = models.CharField(max_length=120)
    name_ar = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(max_length=140, unique=True)
    description_en = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)
    banner = models.ImageField(upload_to="categories/", blank=True)
    icon = models.CharField(max_length=60, blank=True, help_text=_("CSS icon class or emoji fallback"))
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "name_en"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.name_ar if translation.get_language() == "ar" and self.name_ar else self.name_en

    @property
    def description(self):
        return self.description_ar if translation.get_language() == "ar" and self.description_ar else self.description_en

    def get_absolute_url(self):
        return reverse("products:category", kwargs={"slug": self.slug})
