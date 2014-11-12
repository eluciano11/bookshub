from rest_framework import serializers

from .models import Offer, Image


class OfferSerializer(serializers.ModelSerializer):
    owner = serializers.RelatedField()
    book = serializers.RelatedField()

    class Meta:
        model = Offer
        fields = ('owner', 'book', 'price', 'condition',
                  'quantity', 'start_date', 'description')

    def save_object(self, obj, **kwargs):
        obj.owner = self.context['request'].user
        super(OfferSerializer, self).save_object(obj, **kwargs)


class OfferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', )
