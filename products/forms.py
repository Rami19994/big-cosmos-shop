from django import forms

from products.models import ProductQuestion


class ProductQuestionForm(forms.ModelForm):
    class Meta:
        model = ProductQuestion
        fields = ["name", "question"]
