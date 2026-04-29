from django.db import transaction

from orders.models import Invoice, Order, OrderItem
from products.models import StockMovement


@transaction.atomic
def create_order_from_cart(cart, form, user=None):
    order = form.save(commit=False)
    order.user = user if getattr(user, "is_authenticated", False) else None
    method = form.cleaned_data.get("shipping_method_id")
    order.shipping_method = method.name_en if method else "Standard delivery"
    order.shipping_fee = method.base_fee if method else 0
    order.subtotal = cart.subtotal
    order.discount_total = cart.discount_total
    order.coupon_code = cart.coupon.code if cart.coupon else ""
    order.save()
    for item in cart.items.select_related("product", "variant"):
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name_en,
            sku=item.variant.sku if item.variant else item.product.sku,
            variant_label=f"{item.variant.name}: {item.variant.value}" if item.variant else "",
            unit_price=item.unit_price,
            quantity=item.quantity,
            line_total=item.line_total,
        )
        item.product.stock_quantity = max(0, item.product.stock_quantity - item.quantity)
        item.product.save(update_fields=["stock_quantity", "availability", "updated_at"])
        StockMovement.objects.create(product=item.product, variant=item.variant, movement_type=StockMovement.Type.OUT, quantity=item.quantity, note=f"Order {order.order_number}")
    if cart.coupon:
        cart.coupon.used_count += 1
        cart.coupon.save(update_fields=["used_count"])
    Invoice.objects.create(order=order)
    cart.items.all().delete()
    cart.coupon = None
    cart.save(update_fields=["coupon", "updated_at"])
    return order
