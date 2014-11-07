from rest_framework import serializers

from .models import Offer, Image


class OfferSerializer(serializers.ModelSerializer):
    owner = serializers.RelatedField()
    book = serializers.RelatedField()

    class Meta:
        model = Offer
        fields = ('owner', 'book', 'price', 'condition',
                  'quantity', 'start_date', 'end_date', 'description')


class OfferImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', )
