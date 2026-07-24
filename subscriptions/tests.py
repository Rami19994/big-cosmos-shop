from django.contrib.auth.models import User
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse

from subscriptions.models import Store, StoreSubscription, SubscriptionPayment, SubscriptionPlan


class SubscriptionFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="merchant", password="safe-password")
        self.plan = SubscriptionPlan.objects.create(
            code="starter-test", name="Starter", tagline="For testing", monthly_price="9.00", annual_price="90.00", product_limit=25
        )

    def test_customer_can_create_a_pending_store_subscription(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("subscriptions:subscribe", args=[self.plan.code]), {
            "name": "My Store",
            "description": "A new store",
            "billing_cycle": StoreSubscription.BillingCycle.MONTHLY,
        })

        store = Store.objects.get(owner=self.user)
        subscription = StoreSubscription.objects.get(store=store)
        self.assertRedirects(response, reverse("subscriptions:payment", args=[subscription.pk]))
        self.assertEqual(subscription.status, StoreSubscription.Status.PENDING)
        self.assertEqual(subscription.amount, Decimal("9.00"))

    def test_paid_payment_activates_subscription_and_manager_access(self):
        store = Store.objects.create(owner=self.user, name="My Store")
        subscription = StoreSubscription.objects.create(
            store=store, plan=self.plan, billing_cycle=StoreSubscription.BillingCycle.MONTHLY, amount=self.plan.monthly_price
        )
        payment = SubscriptionPayment.objects.create(
            subscription=subscription, method=SubscriptionPayment.Method.BANK, amount=subscription.amount
        )

        payment.status = SubscriptionPayment.Status.PAID
        payment.save(update_fields=["status"])

        subscription.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(subscription.status, StoreSubscription.Status.ACTIVE)
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.groups.filter(name="Store managers").exists())
