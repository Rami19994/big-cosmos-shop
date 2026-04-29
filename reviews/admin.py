from django.contrib import admin
from reviews.models import ProductReview


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "rating", "name", "is_approved", "created_at"]
    list_filter = ["is_approved", "rating"]
    search_fields = ["product__name_en", "name", "comment"]
    actions = ["approve"]

    def approve(self, request, queryset):
        queryset.update(is_approved=True)
