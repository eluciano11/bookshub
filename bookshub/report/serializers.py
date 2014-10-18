from rest_framework import serializers

from .models import ReportedUser, ReportedOffer, ReportedBook


class ReportUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedUser


class ReportOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedOffer


class ReportBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedBook
