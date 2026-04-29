from django.db import models
from django.utils import translation


class ContentPage(models.Model):
    title_en = models.CharField(max_length=160)
    title_ar = models.CharField(max_length=160, blank=True)
    slug = models.SlugField(max_length=180, unique=True)
    body_en = models.TextField()
    body_ar = models.TextField(blank=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def title(self):
        return self.title_ar if translation.get_language() == "ar" and self.title_ar else self.title_en

    @property
    def body(self):
        return self.body_ar if translation.get_language() == "ar" and self.body_ar else self.body_en

    def __str__(self):
        return self.title_en


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=160)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
