from django.contrib import admin
from accounts.models import Address, Profile, RecentlyViewed, SavedPreference, Wishlist

admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Wishlist)
admin.site.register(RecentlyViewed)
admin.site.register(SavedPreference)
