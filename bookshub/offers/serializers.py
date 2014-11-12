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
            "owner_name": self.obj.owner.get_full_name(),
            "owner_username": self.obj.owner.username,
            "book": {
                "title": self.obj.book.title,
                "author": self.obj.book.author,
                "isbn_10": self.obj.book.isbn_10,
                "isbn_13": self.obj.book.isbn_13,
                "edition": self.obj.book.edition,
                "publisher": self.obj.book.publisher,
                "score": self.obj.book.score,
                "tags": self.obj.get_tags_display(),
                "category": self.obj.book.category.name,
                "image": self.obj.book.image.url
            }
        }
        return metadata


class OfferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', )
