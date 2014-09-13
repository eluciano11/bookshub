from django.db import models

from .constants import BOOK_CONDITION

from taggit.managers import TaggableManager


class Book(models.Model):
    description_help_text = """Tell us more about the condition of your book."""

    user = models.ForeignKey('users.User')

    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13, blank=True)
    title = models.CharField(max_length=75, blank=False)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, null=False)
    condition = models.CharField(
        choices=BOOK_CONDITION, blank=False, max_length=10,
        default='new')
    quantity = models.PositiveSmallIntegerField(default=1, null=False)
    author = models.CharField(max_length=50, blank=False)
    edition = models.CharField(max_length=40, blank=False)
    start_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    end_date = models.DateTimeField(null=True)

    description = models.CharField(
        max_length=140, blank=False, help_text=description_help_text)
    publisher = models.CharField(max_length=75)
    tags = TaggableManager()

    def __str__(self):
        return self.title
