from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from blog.models import BlogPost


def listing(request):
    page = Paginator(BlogPost.objects.filter(is_published=True), 9).get_page(request.GET.get("page"))
    return render(request, "blog/list.html", {"page_obj": page})


def detail(request, slug):
    return render(request, "blog/detail.html", {"post": get_object_or_404(BlogPost, slug=slug, is_published=True)})
