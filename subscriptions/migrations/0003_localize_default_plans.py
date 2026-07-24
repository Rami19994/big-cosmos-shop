from django.db import migrations


PLANS = {
    "starter": {
        "name": "Starter", "name_ar": "البداية", "tagline": "A polished start for a new business", "tagline_ar": "لبداية بسيطة واحترافية",
        "features": ["Up to 25 products", "Private management dashboard", "Email support", "Essential analytics"],
        "features_ar": ["حتى 25 منتجًا", "لوحة إدارة خاصة", "دعم عبر البريد الإلكتروني", "إحصاءات أساسية"],
    },
    "growth": {
        "name": "Growth", "name_ar": "النمو", "tagline": "For stores ready to scale", "tagline_ar": "للمتاجر التي تبدأ بالنمو",
        "features": ["Up to 250 products", "Inventory and discounts", "Sales reports", "Priority support"],
        "features_ar": ["حتى 250 منتجًا", "مخزون وخصومات", "تقارير مبيعات", "دعم ذو أولوية"],
    },
    "business": {
        "name": "Business", "name_ar": "الأعمال", "tagline": "Commerce without limits", "tagline_ar": "لتجارة إلكترونية بلا حدود",
        "features": ["Unlimited products", "Advanced reports", "Premium priority support", "Future growth features"],
        "features_ar": ["منتجات غير محدودة", "تقارير متقدمة", "دعم أولوية قصوى", "مزايا توسّع مستقبلية"],
    },
}


def localize_default_plans(apps, schema_editor):
    SubscriptionPlan = apps.get_model("subscriptions", "SubscriptionPlan")
    for code, values in PLANS.items():
        SubscriptionPlan.objects.filter(code=code).update(**values)


class Migration(migrations.Migration):
    dependencies = [("subscriptions", "0002_subscriptionplan_features_ar_and_more")]
    operations = [migrations.RunPython(localize_default_plans, migrations.RunPython.noop)]
