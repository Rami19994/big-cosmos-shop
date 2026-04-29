from django.db import models
from django.utils.translation import gettext_lazy as _


class StoreSetting(models.Model):
    site_name = models.CharField(max_length=120, default="Cosmos Commerce")
    tagline = models.CharField(max_length=180, blank=True)
    logo = models.ImageField(upload_to="settings/", blank=True)
    favicon = models.ImageField(upload_to="settings/", blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    whatsapp = models.CharField(max_length=40, blank=True)
    address_en = models.CharField(max_length=255, blank=True)
    address_ar = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=8, default="USD")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    maintenance_mode = models.BooleanField(default=False)
    homepage_title_en = models.CharField(max_length=160, default="Premium products, delivered beautifully")
    homepage_title_ar = models.CharField(max_length=160, default="منتجات فاخرة تصل إليك بأناقة")
    homepage_subtitle_en = models.TextField(default="A production-ready commerce experience for modern brands.")
    homepage_subtitle_ar = models.TextField(default="تجربة تجارة إلكترونية جاهزة للعلامات التجارية الحديثة.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Store setting")
        verbose_name_plural = _("Store settings")

    def __str__(self):
        return self.site_name
