from time import time

from django.db import models
from django.db.models.signals import post_save

from ..users.models import User
from ..utils.models import BaseModel
from .constants import CATEGORY_CHOICES, REQUEST_STATUS, MULTIPLY_VALUE

from taggit.managers import TaggableManager


def get_book_image_path(self, filename):
        return "uploaded_files/books/%s_%s"\
            % (str(time()).replace('.', '_'), filename)


class Category(BaseModel):
    name = models.CharField(
        choices=CATEGORY_CHOICES, max_length=30, primary_key=True)

    def __str__(self):
        return self.name


class Book(BaseModel):
    category = models.ForeignKey(Category)

    title = models.CharField(max_length=75)
    author = models.CharField(max_length=50)
    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13, blank=True)
    edition = models.CharField(max_length=15, blank=True)
    publisher = models.CharField(max_length=75)
    image = models.ImageField(upload_to=get_book_image_path, blank=True)
    score = models.FloatField(null=True, default=0.0)
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

    def __str__(self):
        return self.review


class Viewed(BaseModel):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)

    def __str__(self):
        return self.book.title


class Requested(BaseModel):
    user = models.ManyToManyField(User)
    status = models.CharField(
        choices=REQUEST_STATUS, max_length=10, default='requested')
    isbn_10 = models.CharField(max_length=10, blank=True)
    isbn_13 = models.CharField(max_length=13, blank=True)
    title = models.CharField(max_length=75)
    author = models.CharField(max_length=50, blank=True)
    count = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.title


def recalculate_total_score(sender, **kwargs):
    c = kwargs['instance']
    if c.score > 0.0:
        reviews = Review.objects.filter(book=c.book.id).exclude(score__lte=0.0)

        accumulator = 0
        score = 0
        count = reviews.count()

        if count > 0:
            for r in reviews:
                accumulator += r.score

            score = accumulator / (count * MULTIPLY_VALUE)

            book = Book.objects.get(id=c.book.id)
            book.score = score

            book.save()

post_save.connect(recalculate_total_score, sender=Review)
