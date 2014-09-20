import math
import datetime

from rest_framework import serializers

from .models import Book, Category
from ..users.models import User
from .constants import CATEGORY_CHOICES, BOOK_CONDITION


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('owner', 'category', 'isbn_10', 'isbn_13', 'title', 'price',
                  'condition', 'quantity', 'author', 'start_date', 'description',
                  'publisher')


class CreateBookSerializer(serializers.Serializer):
    owner = serializers.EmailField()
    category = serializers.ChoiceField(choices=CATEGORY_CHOICES)
    isbn_10 = serializers.CharField(max_length=10, required=False)
    isbn_13 = serializers.CharField(max_length=13, required=False)
    title = serializers.CharField(max_length=75)
    quantity = serializers.IntegerField()
    condition = serializers.ChoiceField(choices=BOOK_CONDITION)
    price = serializers.FloatField()
    author = serializers.CharField(max_length=50)
    edition = serializers.CharField(max_length=10)

    def validate_owner(self, attrs, source):
        owner = attrs[source]

        is_found = User.objects.filter(email__iexact=owner)

        if not is_found:
            message = 'Email does not exist.'
            return serializers.ValidationError(message)

        return attrs

    def create_book(self, attrs):
        owner = User.objects.get(email=attrs['owner'])
        category = Category.objects.get(name=attrs['category'])
        isbn_10 = attrs['isbn_10']
        isbn_13 = attrs['isbn_13']
        title = attrs['title']
        price = attrs['price']
        condition = attrs['condition']
        quantity = attrs['quantity']
        author = attrs['author']
        start_date = datetime.datetime.now()
        edition = attrs['edition']

        b = Book(
            owner=owner, category=category, isbn_10=isbn_10, isbn_13=isbn_13,
            title=title, price=price, condition=condition,
            quantity=quantity, author=author, start_date=start_date,
            edition=edition)
        b.save()
        return b

    def validate(self, attrs):
        book = self.create_book(attrs)
        return BookSerializer(book).data
