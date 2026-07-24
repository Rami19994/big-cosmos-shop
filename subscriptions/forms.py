from django import forms
from django.utils.translation import gettext_lazy as _

from subscriptions.models import Store


class StoreSetupForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3, "placeholder": _("Tell customers about your store")})}


class PaymentMethodForm(forms.Form):
    method = forms.ChoiceField(
        choices=[
            ("bank", _("Bank transfer")),
            ("stripe", _("Credit card via Stripe")),
            ("paypal", "PayPal"),
        ],
        widget=forms.RadioSelect,
    )
