from rest_framework import serializers

from .models import Book, Requested, Review
from ..offers.models import Offer
from ..offers.serializers import OfferSerializer


class BookSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'publisher', 'score',
                  'category', 'isbn_10', 'isbn_13', 'edition')


class BookSerializer(serializers.ModelSerializer):
    tags = serializers.Field(source='get_tags_display')

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'publisher', 'score',
                  'category', 'isbn_10', 'isbn_13', 'edition')

    def save_object(self, obj, **kwargs):
        obj.owner = self.context['request'].user
        super(BookSerializer, self).save_object(obj, **kwargs)


class SearchSerializer(serializers.ModelSerializer):
    offers = serializers.SerializerMethodField('get_book_offers')

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'publisher', 'score',
                  'category', 'isbn_10', 'isbn_13', 'edition', 'offers')

    def get_book_offers(self, obj):
        sort_field = self.context['request'].QUERY_PARAMS.get('sort_field')
        sort_condition = self.context['request'].QUERY_PARAMS.get(
            'sort_condition')

        offers = Offer.objects.filter(book=obj.id)

        if offers and sort_field.lower() == 'price':
            if sort_condition:
                offers = offers.order_by(sort_condition, sort_field)
            else:
                offers = offers.order_by(sort_field)

        elif offers and sort_condition:
            offers = offers.order_by(sort_condition)

        return OfferSerializer(offers).data


class RequestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requested
        fields = ('user', 'status', 'isbn_10',
                  'isbn_13', 'title', 'author', 'count')


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('user', 'book', 'review', 'score')

    def validate(self, attrs):
        review = attrs.get('review')
        score = attrs.get('score')

        if not review and score == 0.0:
            msg = 'Please write a review and/or give a score.'
            raise serializers.ValidationError(msg)

        if review:
            user = attrs['user']
            book = attrs['book']

            reviews = Review.objects.filter(
                user=user, book=book).exclude(score__lte=0.0).count()

            if reviews > 0 and score != 0.0:
                msg = 'You have already scored this book.'
                raise serializers.ValidationError(msg)

        return attrs
