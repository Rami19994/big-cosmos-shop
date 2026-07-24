from django.test import TestCase
from django.urls import reverse

from cart.models import Cart, CartItem
from categories.models import Category
from orders.forms import CheckoutForm
from orders.models import Order
from orders.services import InsufficientStock, create_order_from_cart
from products.models import Product


class OrderAccessTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            email="guest@example.com",
            full_name="Guest Customer",
            phone="123456",
            country="Iraq",
            city="Baghdad",
            address_line1="Test street",
        )

    def test_guest_order_is_not_visible_to_another_session(self):
        response = self.client.get(reverse("orders:confirmation", args=[self.order.order_number]))

        self.assertRedirects(response, reverse("core:home"))

    def test_guest_order_is_visible_to_placing_session(self):
        session = self.client.session
        session["guest_order_numbers"] = [self.order.order_number]
        session.save()

        response = self.client.get(reverse("orders:confirmation", args=[self.order.order_number]))

        self.assertEqual(response.status_code, 200)


class InventoryCheckoutTests(TestCase):
    def test_insufficient_stock_does_not_create_an_order_or_change_inventory(self):
        category = Category.objects.create(name_en="Clothing", slug="clothing")
        product = Product.objects.create(
            category=category,
            name_en="T-Shirt",
            slug="t-shirt",
            sku="TS-001",
            price="10.00",
            stock_quantity=1,
        )
        cart = Cart.objects.create(session_key="test-session")
        CartItem.objects.create(cart=cart, product=product, quantity=2)
        form = CheckoutForm(data={
            "email": "guest@example.com",
            "full_name": "Guest Customer",
            "phone": "123456",
            "country": "Iraq",
            "city": "Baghdad",
            "address_line1": "Test street",
            "payment_method": "cod",
        })
        self.assertTrue(form.is_valid())

        with self.assertRaises(InsufficientStock):
            create_order_from_cart(cart, form)

        product.refresh_from_db()
        self.assertEqual(product.stock_quantity, 1)
        self.assertEqual(Order.objects.count(), 0)
        self.assertTrue(cart.items.exists())
