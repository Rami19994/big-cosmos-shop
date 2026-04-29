from django.contrib import admin
from categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name_en", "parent", "is_featured", "is_active", "sort_order"]
    list_filter = ["is_featured", "is_active"]
    prepopulated_fields = {"slug": ["name_en"]}
    search_fields = ["name_en", "name_ar"]
