import time

from django.db import models
from .constants import BOOK_CONDITION, CATEGORY_CHOICES

from taggit.managers import TaggableManager


def get_book_image_path(filename):
    return "books/%s_%s" % \
           (str(time()).replace('.', '_'), filename)


class Book(models.Model):
    description_help_text = """Tell us more about the condition of your book."""

    user = models.ForeignKey('users.User')
    category = models.ForeignKey('Category')

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


class Review(models.Model):
    user = models.ForeignKey('users.User')
    book = models.ForeignKey('Book')

    review = models.CharField(max_length=200, blank=True)
    score = models.FloatField(default=0.0)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.review


class Image(models.Model):
    book = models.ForeignKey('Book')

    image = models.ImageField(
        upload_to=get_book_image_path, height_field=100,
        width_field=100, blank=True)

    def __str__(self):
        return self.book.title()


class Category(models.Model):
    name = models.CharField(
        choices=CATEGORY_CHOICES, max_length=30, default='accounting')

    def __str__(self):
        return self.name.title()
