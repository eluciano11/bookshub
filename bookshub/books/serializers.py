from rest_framework import serializers

<<<<<<< HEAD
from .models import Book, Requested
=======
from .models import Book, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', )
>>>>>>> FETCH_HEAD


class BookSerializer(serializers.ModelSerializer):
    tags = serializers.Field(source='get_tags_display')

    class Meta:
        model = Book
        fields = ('id', 'title', 'condition', 'price', 'author', 'description',
                  'publisher', 'category', 'isbn_10', 'isbn_13', 'quantity',
                  'edition', 'tags')

    def save_object(self, obj, **kwargs):
        obj.owner = self.context['request'].user
        super(BookSerializer, self).save_object(obj, **kwargs)


class RequestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requested
        fields = ('user', 'status', 'isbn_10', 'isbn_13', 'title', 'author')
