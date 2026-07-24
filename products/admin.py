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
    list_display = ["name_en", "sku", "owner", "category", "brand", "price", "discount_price", "stock_quantity", "availability", "is_active"]
    list_filter = ["availability", "is_featured", "is_best_seller", "is_new_arrival", "category", "brand"]
    search_fields = ["name_en", "name_ar", "sku", "tags"]
    prepopulated_fields = {"slug": ["name_en"]}
    inlines = [ProductImageInline, VariantInline, SpecificationInline]
    filter_horizontal = ["related_products", "upsell_products", "cross_sell_products"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(owner=request.user)

    def _has_active_subscription(self, user):
        if user.is_superuser:
            return True
        return bool(getattr(getattr(user, "store", None), "active_subscription", None))

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj) and self._has_active_subscription(request.user)

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj) and self._has_active_subscription(request.user)

    def has_delete_permission(self, request, obj=None):
        return super().has_delete_permission(request, obj) and self._has_active_subscription(request.user)

    def has_add_permission(self, request):
        if not super().has_add_permission(request):
            return False
        if request.user.is_superuser:
            return True
        subscription = getattr(getattr(request.user, "store", None), "active_subscription", None)
        if not subscription:
            return False
        return not subscription.plan.product_limit or self.get_queryset(request).count() < subscription.plan.product_limit

    def get_exclude(self, request, obj=None):
        excluded = list(super().get_exclude(request, obj) or [])
        if not request.user.is_superuser:
            excluded.append("owner")
        return excluded

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            owned_products = Product.objects.filter(owner=request.user)
            for field_name in ("related_products", "upsell_products", "cross_sell_products"):
                form.base_fields[field_name].queryset = owned_products
        return form

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name"]


admin.site.register(ProductQuestion)
admin.site.register(StockMovement)
