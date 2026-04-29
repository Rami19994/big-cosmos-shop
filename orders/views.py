from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.views import get_cart
from orders.forms import CheckoutForm
from orders.models import Order
from orders.services import create_order_from_cart


def checkout(request):
    cart = get_cart(request)
    if not cart.items.exists():
        messages.info(request, "Your cart is empty.")
        return redirect("cart:detail")
    initial = {}
    if request.user.is_authenticated:
        initial["email"] = request.user.email
        initial["full_name"] = request.user.get_full_name() or request.user.username
        address = request.user.addresses.filter(is_default=True).first()
        if address:
            initial.update({"phone": address.phone, "country": address.country, "city": address.city, "region": address.region, "address_line1": address.address_line1, "address_line2": address.address_line2, "postal_code": address.postal_code})
    form = CheckoutForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        order = create_order_from_cart(cart, form, request.user)
        messages.success(request, "Order placed successfully.")
        return redirect("orders:confirmation", order_number=order.order_number)
    return render(request, "checkout/checkout.html", {"cart": cart, "form": form})


def confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, "orders/confirmation.html", {"order": order})


@login_required
def history(request):
    return render(request, "orders/history.html", {"orders": request.user.orders.all()})


def detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if order.user and order.user != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to view this order.")
        return redirect("core:home")
    return render(request, "orders/detail.html", {"order": order})


@login_required
@require_POST
def cancel(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    if order.can_cancel:
        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])
        messages.success(request, "Order cancelled.")
    return redirect(order.get_absolute_url())


@staff_member_required
def invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, "orders/invoice.html", {"order": order})
