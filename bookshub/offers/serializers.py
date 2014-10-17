from rest_framework import serializers

from .models import Offer


class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
