from django.contrib import admin

from wishlist.models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "created_at",
        "updated_at",
    )
