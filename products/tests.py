from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse

from categories.models import Category
from products.models import Product
from subscriptions.models import Store, StoreSubscription, SubscriptionPlan


class StoreManagerAdminTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(username="store-manager", password="safe-password", is_staff=True)
        other_user = User.objects.create_user(username="other-manager", password="safe-password", is_staff=True)
        permissions = Permission.objects.filter(
            content_type__app_label="products",
            content_type__model="product",
            codename__in=["add_product", "change_product", "delete_product", "view_product"],
        )
        group = Group.objects.create(name="Store managers")
        group.permissions.set(permissions)
        self.manager.groups.add(group)

        plan = SubscriptionPlan.objects.create(
            code="test-plan", name="Test plan", tagline="Test", monthly_price="9.00", annual_price="90.00", product_limit=25
        )
        store = Store.objects.create(owner=self.manager, name="Manager store")
        subscription = StoreSubscription.objects.create(
            store=store, plan=plan, billing_cycle=StoreSubscription.BillingCycle.MONTHLY
        )
        subscription.activate()

        category = Category.objects.create(name_en="Clothing", slug="clothing")
        self.own_product = Product.objects.create(category=category, owner=self.manager, name_en="My product", slug="my-product", sku="MINE-001", price="10.00")
        self.other_product = Product.objects.create(category=category, owner=other_user, name_en="Private product", slug="private-product", sku="OTHER-001", price="10.00")

    def test_manager_sees_only_own_products_in_django_admin(self):
        self.client.force_login(self.manager)

        response = self.client.get(reverse("admin:products_product_changelist"))

        self.assertContains(response, self.own_product.name_en)
        self.assertNotContains(response, self.other_product.name_en)

    def test_manager_cannot_open_custom_global_dashboard(self):
        self.client.force_login(self.manager)

        response = self.client.get(reverse("dashboard:home"))

        self.assertEqual(response.status_code, 302)
