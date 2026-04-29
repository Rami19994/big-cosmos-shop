from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone, translation
from django.utils.text import slugify


class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    title_en = models.CharField(max_length=180)
    title_ar = models.CharField(max_length=180, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt_en = models.CharField(max_length=255, blank=True)
    excerpt_ar = models.CharField(max_length=255, blank=True)
    body_en = models.TextField()
    body_ar = models.TextField(blank=True)
    cover = models.ImageField(upload_to="blog/", blank=True)
    tags = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def title(self):
        return self.title_ar if translation.get_language() == "ar" and self.title_ar else self.title_en

    @property
    def excerpt(self):
        return self.excerpt_ar if translation.get_language() == "ar" and self.excerpt_ar else self.excerpt_en

    @property
    def body(self):
        return self.body_ar if translation.get_language() == "ar" and self.body_ar else self.body_en

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
