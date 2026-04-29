from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from pages.forms import ContactForm
from pages.models import ContentPage


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Message sent. Our support team will reply soon.")
        return redirect("pages:contact")
    return render(request, "pages/contact.html", {"form": form})


def page(request, slug):
    return render(request, "pages/page.html", {"page": get_object_or_404(ContentPage, slug=slug, is_published=True)})


def about(request):
    return render(request, "pages/about.html")


def faq(request):
    return render(request, "pages/faq.html")
