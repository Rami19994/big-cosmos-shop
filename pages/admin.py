from django.contrib import admin
from pages.models import ContactMessage, ContentPage


@admin.register(ContentPage)
class ContentPageAdmin(admin.ModelAdmin):
    list_display = ["title_en", "slug", "is_published", "updated_at"]
    prepopulated_fields = {"slug": ["title_en"]}

admin.site.register(ContactMessage)
