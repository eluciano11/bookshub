from django.contrib import admin

from .models import Cart

from reversion import VersionAdmin


class CartAdmin(VersionAdmin):
    list_display = ('buyer', 'quantity')

admin.site.register(Cart, CartAdmin)
