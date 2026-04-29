from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from categories.models import Category
from core.models import StoreSetting
from pages.models import ContentPage
from products.models import Brand, Product, ProductSpecification
from marketing.models import Banner, Testimonial
from orders.models import ShippingMethod


class Command(BaseCommand):
    help = "Create demo storefront data for local development."

    def handle(self, *args, **options):
        StoreSetting.objects.get_or_create(site_name="Nova Commerce", defaults={"tagline": "Premium retail, engineered for growth", "email": "support@example.com", "phone": "+100000000", "whatsapp": "100000000"})
        for slug, title, body in [
            ("about", "About us", "Nova Commerce is a modern store experience for ambitious retailers."),
            ("faq", "FAQ", "Find answers about delivery, returns, payments, and support."),
            ("terms", "Terms and conditions", "Use this page to publish store terms."),
            ("privacy", "Privacy policy", "Use this page to publish privacy practices."),
            ("returns", "Return and refund policy", "Use this page to explain returns and refunds."),
            ("shipping", "Shipping policy", "Use this page to explain shipping zones and timing."),
        ]:
            ContentPage.objects.get_or_create(slug=slug, defaults={"title_en": title, "title_ar": title, "body_en": body, "body_ar": body})
        brand, _ = Brand.objects.get_or_create(slug="nova", defaults={"name": "Nova"})
        categories = []
        for name, icon in [("Electronics", "◈"), ("Fashion", "◆"), ("Home", "◇"), ("Beauty", "✦")]:
            cat, _ = Category.objects.get_or_create(slug=slugify(name), defaults={"name_en": name, "name_ar": name, "icon": icon, "is_featured": True})
            categories.append(cat)
        for i in range(1, 9):
            product, _ = Product.objects.get_or_create(
                sku=f"NOVA-{i:03d}",
                defaults={"category": categories[i % len(categories)], "brand": brand, "name_en": f"Signature Product {i}", "name_ar": f"منتج مميز {i}", "price": Decimal("99.00") + i, "discount_price": Decimal("79.00") + i if i % 2 == 0 else None, "stock_quantity": 25 + i, "is_active": True, "is_featured": True, "is_new_arrival": i > 4, "is_best_seller": i <= 4, "summary_en": "A premium product card ready for real catalog data.", "description_en": "Detailed product copy, specifications, media, variants, reviews, and Q&A are supported."},
            )
            ProductSpecification.objects.get_or_create(product=product, name_en="Material", defaults={"value_en": "Premium grade"})
        Banner.objects.get_or_create(title_en="Seasonal edit", defaults={"subtitle_en": "Premium picks for the month", "placement": "home", "is_active": True})
        Testimonial.objects.get_or_create(name="Amina", defaults={"quote_en": "The storefront feels fast, polished, and trustworthy.", "quote_ar": "المتجر سريع وأنيق وموثوق.", "rating": 5})
        ShippingMethod.objects.get_or_create(name_en="Standard delivery", defaults={"name_ar": "توصيل عادي", "base_fee": Decimal("5.00")})
        ShippingMethod.objects.get_or_create(name_en="Pickup from store", defaults={"name_ar": "استلام من المتجر", "method_type": "pickup", "base_fee": Decimal("0.00")})
        self.stdout.write(self.style.SUCCESS("Demo data created."))
