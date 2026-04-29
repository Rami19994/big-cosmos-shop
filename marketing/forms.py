from django import forms

from marketing.models import NewsletterSubscription


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ["email"]
