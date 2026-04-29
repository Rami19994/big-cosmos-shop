from django import forms

from reviews.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["name", "rating", "title", "comment"]
