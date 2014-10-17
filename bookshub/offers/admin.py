from django.contrib import admin

from .models import Offer, Image

from reversion import VersionAdmin


class OfferAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = (
        'book', 'owner', 'price', 'quantity', 'start_date',)


class ImageAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('offer', 'image',)

admin.site.register(Offer, OfferAdmin)
admin.site.register(Image, ImageAdmin)
