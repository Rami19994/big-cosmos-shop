from django.contrib import admin
from products.models import Brand, Product, ProductImage, ProductQuestion, ProductSpecification, ProductVariant, StockMovement


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class VariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class SpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name_en", "sku", "category", "brand", "price", "discount_price", "stock_quantity", "availability", "is_active"]
    list_filter = ["availability", "is_featured", "is_best_seller", "is_new_arrival", "category", "brand"]
    search_fields = ["name_en", "name_ar", "sku", "tags"]
    prepopulated_fields = {"slug": ["name_en"]}
    inlines = [ProductImageInline, VariantInline, SpecificationInline]
    filter_horizontal = ["related_products", "upsell_products", "cross_sell_products"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name"]


admin.site.register(ProductQuestion)
admin.site.register(StockMovement)
