from rest_framework import serializers

from .models import ReportedUser


class ReportUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedUser
