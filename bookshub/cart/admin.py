from django.contrib import admin

from .models import OrderItem

from reversion import VersionAdmin


class OrderItemAdmin(VersionAdmin):
<<<<<<< HEAD
    list_display = ('offer', 'user', 'quantity', 'is_purchased')
=======
    list_display = ('user', 'offer', 'quantity', 'is_purchased')
>>>>>>> FETCH_HEAD

admin.site.register(OrderItem, OrderItemAdmin)
