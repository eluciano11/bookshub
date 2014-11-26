from time import time

from django.db import models

from .constants import BOOK_CONDITION
from ..users.models import User
from ..books.models import Book
from ..utils.models import BaseModel

from django_filepicker.models import FPFileField


class Offer(BaseModel):
    class Meta:
        ordering = ['price', 'condition']
    description_help_text = "Tell us more about the condition of your book."
    owner = models.ForeignKey(User)
    book = models.ForeignKey(Book)

    price = models.DecimalField(max_digits=5, decimal_places=2)
    condition = models.CharField(choices=BOOK_CONDITION, max_length=10)
    quantity = models.PositiveSmallIntegerField(default=1)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    description = models.CharField(
        max_length=140, help_text=description_help_text)

    def __str__(self):
        return self.owner.email


class Image(BaseModel):
    offer = models.ForeignKey(Offer)

    def get_book_image_path(self, filename):
        return "uploaded_files/books/%s_%s"\
            % (str(time()).replace('.', '_'), filename)

    image = FPFileField(upload_to=get_book_image_path)

    def __str__(self):
        return self.offer.description
