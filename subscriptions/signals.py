from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from subscriptions.models import StoreSubscription, SubscriptionPayment


DEFAULT_PLANS = [
    {"code": "starter", "name": "Starter", "name_ar": "البداية", "tagline": "A polished start for a new business", "tagline_ar": "لبداية بسيطة واحترافية", "monthly_price": "9.00", "annual_price": "90.00", "product_limit": 25, "features": ["Up to 25 products", "Private management dashboard", "Email support", "Essential analytics"], "features_ar": ["حتى 25 منتجًا", "لوحة إدارة خاصة", "دعم عبر البريد الإلكتروني", "إحصاءات أساسية"], "sort_order": 1},
    {"code": "growth", "name": "Growth", "name_ar": "النمو", "tagline": "For stores ready to scale", "tagline_ar": "للمتاجر التي تبدأ بالنمو", "monthly_price": "24.00", "annual_price": "240.00", "product_limit": 250, "features": ["Up to 250 products", "Inventory and discounts", "Sales reports", "Priority support"], "features_ar": ["حتى 250 منتجًا", "مخزون وخصومات", "تقارير مبيعات", "دعم ذو أولوية"], "is_popular": True, "sort_order": 2},
    {"code": "business", "name": "Business", "name_ar": "الأعمال", "tagline": "Commerce without limits", "tagline_ar": "لتجارة إلكترونية بلا حدود", "monthly_price": "59.00", "annual_price": "590.00", "product_limit": 0, "features": ["Unlimited products", "Advanced reports", "Premium priority support", "Future growth features"], "features_ar": ["منتجات غير محدودة", "تقارير متقدمة", "دعم أولوية قصوى", "مزايا توسّع مستقبلية"], "sort_order": 3},
]


def _sync_store_manager_access(subscription):
    user = subscription.store.owner
    group, _ = Group.objects.get_or_create(name="Store managers")
    permissions = Permission.objects.filter(
        content_type__app_label="products",
        content_type__model="product",
        codename__in=["add_product", "change_product", "delete_product", "view_product"],
    )
    group.permissions.set(permissions)
    has_active_subscription = user.store.subscriptions.filter(
        status=StoreSubscription.Status.ACTIVE,
        current_period_end__gte=timezone.now(),
    ).exists()
    if has_active_subscription:
        user.groups.add(group)
        if not user.is_staff:
            user.is_staff = True
            user.save(update_fields=["is_staff"])
    else:
        user.groups.remove(group)


@receiver(post_save, sender=StoreSubscription)
def sync_store_manager_access(sender, instance, **kwargs):
    _sync_store_manager_access(instance)


@receiver(post_save, sender=SubscriptionPayment)
def activate_paid_subscription(sender, instance, **kwargs):
    if instance.status == SubscriptionPayment.Status.PAID and instance.subscription.status != StoreSubscription.Status.ACTIVE:
        instance.subscription.activate()


def seed_default_plans(sender, **kwargs):
    from subscriptions.models import SubscriptionPlan

    for plan in DEFAULT_PLANS:
        SubscriptionPlan.objects.get_or_create(code=plan["code"], defaults=plan)
