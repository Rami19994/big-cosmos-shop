from django import forms

from orders.models import Order, ShippingMethod


class CheckoutForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=[("cod", "Cash on delivery"), ("bank", "Bank transfer"), ("stripe", "Stripe ready"), ("paypal", "PayPal ready")])
    shipping_method_id = forms.ModelChoiceField(queryset=ShippingMethod.objects.filter(is_active=True), required=False, empty_label="Standard delivery")
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False, widget=forms.HiddenInput())
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False, widget=forms.HiddenInput())

    class Meta:
        model = Order
        fields = ["email", "full_name", "phone", "country", "city", "region", "address_line1", "address_line2", "postal_code", "notes", "payment_method", "latitude", "longitude"]
