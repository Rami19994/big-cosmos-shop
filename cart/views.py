from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.models import Cart, CartItem
from coupons.models import Coupon
from products.models import Product, ProductVariant


def _session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_cart(request):
    if not hasattr(request, "session"):
        return Cart()
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        anonymous = Cart.objects.filter(session_key=request.session.session_key, user__isnull=True).first()
        if anonymous and anonymous.pk != cart.pk:
            for item in anonymous.items.all():
                existing, created = CartItem.objects.get_or_create(cart=cart, product=item.product, variant=item.variant, defaults={"quantity": item.quantity})
                if not created:
                    existing.quantity += item.quantity
                    existing.save()
            anonymous.delete()
        return cart
    cart, _ = Cart.objects.get_or_create(session_key=_session_key(request), user__isnull=True)
    return cart


def detail(request):
    return render(request, "cart/detail.html", {"cart": get_cart(request)})


@require_POST
def add(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    variant = None
    if request.POST.get("variant"):
        variant = get_object_or_404(ProductVariant, pk=request.POST["variant"], product=product)
    quantity = max(1, int(request.POST.get("quantity", 1)))
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, variant=variant, defaults={"quantity": quantity})
    if not created:
        item.quantity += quantity
        item.save()
    messages.success(request, "Product added to cart.")
    return redirect(request.POST.get("next") or "cart:detail")


@require_POST
def update(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart=get_cart(request))
    item.quantity = max(1, int(request.POST.get("quantity", 1)))
    item.save()
    return redirect("cart:detail")


@require_POST
def remove(request, item_id):
    get_object_or_404(CartItem, pk=item_id, cart=get_cart(request)).delete()
    return redirect("cart:detail")


@require_POST
def apply_coupon(request):
    cart = get_cart(request)
    code = request.POST.get("code", "").strip().upper()
    coupon = Coupon.objects.filter(code__iexact=code).first()
    if coupon and coupon.is_valid_for(cart.subtotal):
        cart.coupon = coupon
        cart.save()
        messages.success(request, "Coupon applied.")
    else:
        messages.error(request, "Invalid coupon.")
    return redirect("cart:detail")
