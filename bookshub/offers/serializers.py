from rest_framework import serializers

from .models import Offer, Image
from books.serializers import BookSimpleSerializer


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
            "book": BookSimpleSerializer(obj.book)
        }
        return metadata


class OfferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', )
