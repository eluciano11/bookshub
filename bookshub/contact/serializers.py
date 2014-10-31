from rest_framework import serializers

from .models import Message


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
