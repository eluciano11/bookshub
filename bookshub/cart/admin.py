from django.contrib import admin

from .models import OrderItem

from reversion import VersionAdmin


class OrderItemAdmin(VersionAdmin):
    list_display = ('user', 'offer', 'quantity', 'is_purchased')

admin.site.register(OrderItem, OrderItemAdmin)
