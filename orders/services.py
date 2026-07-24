from collections import defaultdict

from django.db import transaction

from orders.models import Invoice, Order, OrderItem
from products.models import Product, ProductVariant, StockMovement


class InsufficientStock(Exception):
    """Raised when an item can no longer be fulfilled at checkout."""


@transaction.atomic
def create_order_from_cart(cart, form, user=None):
    # Lock the cart and inventory rows so simultaneous checkouts cannot both
    # consume the same units. PostgreSQL enforces these row locks in production.
    cart = cart.__class__.objects.select_for_update().get(pk=cart.pk)
    cart_items = list(cart.items.select_related("product", "variant"))
    product_quantities = defaultdict(int)
    variant_quantities = defaultdict(int)
    for item in cart_items:
        product_quantities[item.product_id] += item.quantity
        if item.variant_id:
            variant_quantities[item.variant_id] += item.quantity

    products = Product.objects.select_for_update().in_bulk(product_quantities)
    variants = ProductVariant.objects.select_for_update().in_bulk(variant_quantities)
    for product_id, quantity in product_quantities.items():
        product = products[product_id]
        if not product.is_active or (
            product.availability != Product.Availability.PREORDER
            and product.stock_quantity < quantity
        ):
            raise InsufficientStock(f"{product.name_en} is no longer available in the requested quantity.")
    for variant_id, quantity in variant_quantities.items():
        variant = variants[variant_id]
        if variant.stock_quantity < quantity:
            raise InsufficientStock(f"{variant} is no longer available in the requested quantity.")

    order = form.save(commit=False)
    order.user = user if getattr(user, "is_authenticated", False) else None
    method = form.cleaned_data.get("shipping_method_id")
    order.shipping_method = method.name_en if method else "Standard delivery"
    order.shipping_fee = method.base_fee if method else 0
    order.subtotal = cart.subtotal
    order.discount_total = cart.discount_total
    order.coupon_code = cart.coupon.code if cart.coupon else ""
    order.save()
    for item in cart_items:
        product = products[item.product_id]
        variant = variants.get(item.variant_id)
        unit_price = product.current_price + (variant.price_delta if variant else 0)
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name_en,
            sku=variant.sku if variant else product.sku,
            variant_label=f"{variant.name}: {variant.value}" if variant else "",
            unit_price=unit_price,
            quantity=item.quantity,
            line_total=unit_price * item.quantity,
        )
        product.stock_quantity = max(0, product.stock_quantity - item.quantity)
        if variant:
            variant.stock_quantity -= item.quantity
            variant.save(update_fields=["stock_quantity"])
        StockMovement.objects.create(product=product, variant=variant, movement_type=StockMovement.Type.OUT, quantity=item.quantity, note=f"Order {order.order_number}")
    for product in products.values():
        product.save(update_fields=["stock_quantity", "availability", "updated_at"])
    if cart.coupon:
        cart.coupon.used_count += 1
        cart.coupon.save(update_fields=["used_count"])
    Invoice.objects.create(order=order)
    cart.items.all().delete()
    cart.coupon = None
    cart.save(update_fields=["coupon", "updated_at"])
    return order
