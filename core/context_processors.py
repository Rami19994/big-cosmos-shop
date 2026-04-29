def storefront(request):
    from cart.views import get_cart
    from core.models import StoreSetting

    from django.db import OperationalError, ProgrammingError
    try:
        setting = StoreSetting.objects.first()
        cart = get_cart(request)
    except (OperationalError, ProgrammingError):
        setting = None
        cart = None
    return {
        "store": setting,
        "cart_count": cart.items.count() if cart and cart.pk else 0,
        "is_rtl": getattr(request, "LANGUAGE_CODE", "en") == "ar",
    }
