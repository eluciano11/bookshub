from time import time

from django.db import models

from ..users.models import User
from ..utils.models import BaseModel
from .constants import BOOK_CONDITION, CATEGORY_CHOICES, REQUEST_STATUS
from jsonfield import JSONField

from taggit.managers import TaggableManager


class Category(BaseModel):
    name = models.CharField(
        choices=CATEGORY_CHOICES, max_length=30, primary_key=True)

    def __str__(self):
        return self.name


class Book(BaseModel):
    description_help_text = "Tell us more about the condition of your book."

    owner = models.ForeignKey(User)
    category = models.ForeignKey(Category)

    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13, blank=True)
    title = models.CharField(max_length=75)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    condition = models.CharField(choices=BOOK_CONDITION, max_length=10)
    quantity = models.PositiveSmallIntegerField(default=1)
    author = models.CharField(max_length=50)
    edition = models.CharField(max_length=15, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)

    description = models.CharField(
        max_length=140, help_text=description_help_text)
    publisher = models.CharField(max_length=75)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_tags_display(self):
        return self.tags.values_list('name', flat=True)


class Review(BaseModel):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)

    review = models.CharField(max_length=200, blank=True)
    score = models.FloatField(default=0.0)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review


class Image(BaseModel):
    book = models.ForeignKey(Book)

    def get_book_image_path(self, filename):
        return "uploaded_files/books/%s_%s"\
            % (str(time()).replace('.', '_'), filename)

    image = models.ImageField(upload_to=get_book_image_path)

    def __str__(self):
        return self.book


class Viewed(BaseModel):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)

    def __str__(self):
        return self.book


class Requested(BaseModel):
    user = models.ForeignKey(User)
    status = models.CharField(
        choices=REQUEST_STATUS, max_length=10, default='requested')
    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13, blank=True)
    title = models.CharField(max_length=75, blank=True)
    author = models.CharField(max_length=50, blank=True)
    extra_data = JSONField()

    def __str__(self):
        return self.id
