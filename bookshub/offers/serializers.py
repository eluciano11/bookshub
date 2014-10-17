from rest_framework import serializers

from .models import Offer, Image


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer


class OfferImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'image', )
