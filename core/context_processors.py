def storefront(request):
    from cart.views import get_cart
    from core.models import StoreSetting

    setting = StoreSetting.objects.first()
    cart = get_cart(request)
    return {
        "store": setting,
        "cart_count": cart.items.count() if cart.pk else 0,
        "is_rtl": getattr(request, "LANGUAGE_CODE", "en") == "ar",
    }
