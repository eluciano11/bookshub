from rest_framework import serializers

from .models import ReportedUser, ReportedOffer, ReportedBook


class ReportUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedUser

    def validate(self, attrs):
        receiver = attrs['receiver']
        sender = attrs['sender']

        for s in sender:
            if receiver.email == s.email:
                message = 'Invalid action, a user cannot report himself.'
                raise serializers.ValidationError(message)

        return attrs


class ReportOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedOffer

    def validate(self, attrs):
        offer = attrs['offer']
        sender = attrs['sender']

        if offer.owner.email == sender.email:
            message = 'Invalid action, a user cannot report his own offer.'
            raise serializers.ValidationError(message)

        return attrs


class ReportBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedBook
