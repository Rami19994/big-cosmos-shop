from django.contrib import admin

from subscriptions.models import Store, StoreSubscription, SubscriptionPayment, SubscriptionPlan


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "monthly_price", "annual_price", "product_limit", "is_popular", "is_active"]
    prepopulated_fields = {"code": ["name"]}


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "is_active", "created_at"]
    search_fields = ["name", "owner__username", "owner__email"]


@admin.register(StoreSubscription)
class StoreSubscriptionAdmin(admin.ModelAdmin):
    list_display = ["store", "plan", "billing_cycle", "status", "amount", "current_period_end"]
    list_filter = ["status", "billing_cycle", "plan"]
    search_fields = ["store__name", "store__owner__username"]
    actions = ["activate_subscriptions"]

    @admin.action(description="Activate selected subscriptions")
    def activate_subscriptions(self, request, queryset):
        for subscription in queryset:
            subscription.activate()


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ["reference", "subscription", "method", "amount", "status", "created_at"]
    list_filter = ["method", "status"]
    search_fields = ["reference", "subscription__store__name"]
