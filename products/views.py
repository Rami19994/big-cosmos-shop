from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import RecentlyViewed, Wishlist
from categories.models import Category
from products.forms import ProductQuestionForm
from products.models import Brand, Product
from reviews.forms import ProductReviewForm


def _filtered_products(request):
    qs = Product.objects.filter(is_active=True).select_related("category", "brand").prefetch_related("images").annotate(avg_rating=Avg("reviews__rating"))
    q = request.GET.get("q")
    if q:
        qs = qs.filter(Q(name_en__icontains=q) | Q(name_ar__icontains=q) | Q(sku__icontains=q) | Q(tags__icontains=q))
    if request.GET.get("category"):
        qs = qs.filter(category__slug=request.GET["category"])
    if request.GET.get("brand"):
        qs = qs.filter(brand__slug=request.GET["brand"])
    if request.GET.get("availability"):
        qs = qs.filter(availability=request.GET["availability"])
    if request.GET.get("discount"):
        qs = qs.filter(discount_price__isnull=False)
    if request.GET.get("min_price"):
        qs = qs.filter(price__gte=request.GET["min_price"])
    if request.GET.get("max_price"):
        qs = qs.filter(price__lte=request.GET["max_price"])
    if request.GET.get("rating"):
        qs = qs.filter(avg_rating__gte=request.GET["rating"])
    sort = request.GET.get("sort", "newest")
    ordering = {"price_asc": "price", "price_desc": "-price", "popular": "-views", "rating": "-avg_rating", "newest": "-created_at"}
    return qs.order_by(ordering.get(sort, "-created_at"))


def listing(request):
    paginator = Paginator(_filtered_products(request), 12)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "products/list.html", {"page_obj": page, "categories": Category.objects.filter(is_active=True), "brands": Brand.objects.all()})


def category(request, slug):
    cat = get_object_or_404(Category, slug=slug, is_active=True)
    request.GET = request.GET.copy()
    request.GET["category"] = slug
    context = {"category": cat, "page_obj": Paginator(_filtered_products(request), 12).get_page(request.GET.get("page")), "categories": Category.objects.filter(is_active=True), "brands": Brand.objects.all()}
    return render(request, "products/category.html", context)


def detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category", "brand").prefetch_related("images", "variants", "specifications", "related_products"), slug=slug, is_active=True)
    product.views += 1
    product.save(update_fields=["views"])
    if request.user.is_authenticated:
        RecentlyViewed.objects.update_or_create(user=request.user, product=product, defaults={})
    else:
        if not request.session.session_key:
            request.session.create()
        RecentlyViewed.objects.update_or_create(session_key=request.session.session_key, product=product, defaults={})
    review_form = ProductReviewForm(request.POST or None, prefix="review")
    question_form = ProductQuestionForm(request.POST or None, prefix="question")
    if request.method == "POST":
        if "submit_review" in request.POST and review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user if request.user.is_authenticated else None
            review.save()
            messages.success(request, "Review submitted for moderation.")
            return redirect(product.get_absolute_url())
        if "submit_question" in request.POST and question_form.is_valid():
            question = question_form.save(commit=False)
            question.product = product
            question.user = request.user if request.user.is_authenticated else None
            question.save()
            messages.success(request, "Question submitted.")
            return redirect(product.get_absolute_url())
    return render(request, "products/detail.html", {"product": product, "review_form": review_form, "question_form": question_form, "related": product.related_products.filter(is_active=True)[:4]})


def search(request):
    return listing(request)


def suggestions(request):
    q = request.GET.get("q", "")[:50]
    data = list(Product.objects.filter(is_active=True, name_en__icontains=q).values("name_en", "slug")[:8]) if q else []
    return JsonResponse({"results": data})


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
        messages.info(request, "Removed from wishlist.")
    else:
        messages.success(request, "Added to wishlist.")
    return redirect(request.POST.get("next") or product.get_absolute_url())


def compare_add(request, product_id):
    compare = request.session.get("compare", [])
    if product_id not in compare:
        compare.append(product_id)
    request.session["compare"] = compare[:4]
    return redirect("products:compare")


def compare(request):
    products = Product.objects.filter(id__in=request.session.get("compare", [])).prefetch_related("specifications")
    return render(request, "products/compare.html", {"products": products})
