from django.conf import settings

from django.db import models
from django.db.models.signals import post_save
from django.core.mail import send_mail

from ..utils.models import BaseModel
from .constants import CATEGORY_CHOICES, STATUS_CHOICES
from ..users.models import User


class Message(BaseModel):
    user = models.ForeignKey(User)
    subject = models.CharField(max_length=25, blank=False)
    body = models.CharField(max_length=300, blank=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)

    def __str__(self):
        return self.subject


def send_to_bookshub(sender, **kwargs):
    e = kwargs['instance']
    subject = e.category + ' - ' + e.subject
    send_mail(subject, e.body, e.user,
              [settings.BOOKSHUB_EMAIL], fail_silently=False)

post_save.connect(send_to_bookshub, sender=Message)
