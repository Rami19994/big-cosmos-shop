import csv

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render

from blog.models import BlogPost
from categories.models import Category
from marketing.forms import NewsletterForm
from marketing.models import Banner, Testimonial
from orders.models import Order
from products.models import Product


def home(request):
    newsletter_form = NewsletterForm(request.POST or None)
    if request.method == "POST" and newsletter_form.is_valid():
        newsletter_form.save()
    return render(request, "home.html", {
        "newsletter_form": newsletter_form,
        "banners": Banner.objects.filter(is_active=True, placement="home")[:3],
        "categories": Category.objects.filter(is_active=True, is_featured=True)[:8],
        "featured_products": Product.objects.filter(is_active=True, is_featured=True).prefetch_related("images")[:8],
        "best_sellers": Product.objects.filter(is_active=True, is_best_seller=True).prefetch_related("images")[:8],
        "new_arrivals": Product.objects.filter(is_active=True, is_new_arrival=True).prefetch_related("images")[:8],
        "testimonials": Testimonial.objects.filter(is_active=True)[:4],
        "posts": BlogPost.objects.filter(is_published=True)[:3],
    })


@staff_member_required
def dashboard(request):
    orders = Order.objects.all()
    stats = {
        "sales": orders.aggregate(total=Sum("total"))["total"] or 0,
        "orders": orders.count(),
        "customers": User.objects.filter(is_staff=False).count(),
        "products": Product.objects.count(),
    }
    return render(request, "admin/dashboard.html", {"stats": stats, "recent_orders": orders[:8], "low_stock": Product.objects.filter(stock_quantity__lte=5)[:10], "best_products": Product.objects.filter(is_best_seller=True)[:8]})


@staff_member_required
def manage_products(request):
    return render(request, "admin/management.html", {"title": "Product management", "items": Product.objects.select_related("category", "brand")[:100]})


@staff_member_required
def manage_orders(request):
    return render(request, "admin/orders.html", {"orders": Order.objects.all()[:100]})


@staff_member_required
def manage_customers(request):
    return render(request, "admin/customers.html", {"customers": User.objects.filter(is_staff=False)[:100]})


@staff_member_required
def inventory(request):
    return render(request, "admin/inventory.html", {"products": Product.objects.order_by("stock_quantity")[:100]})


@staff_member_required
def reports(request):
    return render(request, "admin/reports.html", {"orders_by_status": Order.objects.values("status").annotate(total=Count("id"))})


@staff_member_required
def settings(request):
    from core.models import StoreSetting
    return render(request, "admin/settings.html", {"setting": StoreSetting.objects.first()})


@staff_member_required
def export_orders(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)
    writer.writerow(["Order", "Customer", "Email", "Status", "Total", "Created"])
    for order in Order.objects.all():
        writer.writerow([order.order_number, order.full_name, order.email, order.status, order.total, order.created_at])
    return response
