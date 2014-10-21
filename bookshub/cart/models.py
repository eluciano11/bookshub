from django.db import models
from django.db.models.signals import pre_save

from ..offers.models import Offer
from ..users.models import User
from ..utils.models import BaseModel


class Cart(BaseModel):
    buyer = models.ForeignKey(User)
    offer = models.ForeignKey(Offer)

    quantity = models.SmallIntegerField(default=1)
    total = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    REQUIRED_FIELDS = ['buyer', 'offer', 'quantity']


def calculate_total(sender, **kwargs):
    t = kwargs['instance']

    total = t.offer.price * t.quantity
    t.total = total

pre_save.connect(calculate_total, sender=Cart)
