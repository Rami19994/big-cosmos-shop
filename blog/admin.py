from django.contrib import admin
from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title_en", "is_published", "published_at"]
    prepopulated_fields = {"slug": ["title_en"]}
    search_fields = ["title_en", "title_ar", "body_en"]
