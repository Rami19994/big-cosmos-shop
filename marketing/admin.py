from django.contrib import admin
from marketing.models import Banner, FlashSale, NewsletterSubscription, Testimonial

admin.site.register(Banner)
admin.site.register(Testimonial)
admin.site.register(NewsletterSubscription)
admin.site.register(FlashSale)
