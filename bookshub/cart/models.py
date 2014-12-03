from django.db import models

from ..offers.models import Offer
from ..users.models import User
from ..utils.models import BaseModel


class OrderItem(BaseModel):
    offer = models.ForeignKey(Offer)
    user = models.ForeignKey(User)

    quantity = models.PositiveIntegerField(default=1)
    purchased_date = models.DateTimeField(auto_now=True)
    is_purchased = models.BooleanField(default=False)
    seller_has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_cart_items(self):
        return OrderItem.objects.filter(user=self.user, is_purchased=False)

    def get_cart_total(self):
        total = 0
        items = self.get_cart_items()
        for item in items:
            total += item.offer.price * item.quantity
        return total
