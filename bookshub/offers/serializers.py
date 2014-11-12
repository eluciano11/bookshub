from rest_framework import serializers

from .models import Offer, Image


# class BookSimpleSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Book
#         fields = ('id', 'title', 'author', 'publisher', 'score',
#                   'category', 'isbn_10', 'isbn_13', 'edition')


class OfferSerializer(serializers.ModelSerializer):
    metadata = serializers.SerializerMethodField('get_metadata')

    class Meta:
        model = Offer
        fields = ('id', 'owner', 'book', 'price', 'condition',
                  'quantity', 'start_date', 'description', 'metadata')

    def save_object(self, obj, **kwargs):
        obj.owner = self.context['request'].user
        super(OfferSerializer, self).save_object(obj, **kwargs)

    def get_metadata(self, obj):
        metadata = {
            "owner_name": obj.owner.get_full_name(),
            "owner_username": obj.owner.username,
            "book": {
                "title": obj.book.title,
                "author": obj.book.author,
                "isbn_10": obj.book.isbn_10,
                "isbn_13": obj.book.isbn_13,
                "edition": obj.book.edition,
                "publisher": obj.book.publisher,
                "score": obj.book.score,
                "tags": obj.book.get_tags_display(),
                "category": obj.book.category.name,
                # "image": obj.book.image.url
            }
        }
        return metadata


class OfferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', )
