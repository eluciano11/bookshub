from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User
from ..utils.serializers import DynamicFieldsModelSerializer
from ..utils import fields


class SigninSerializer(serializers.Serializer):
    """
    Serializer that handles signin endpoint data.
    """
    email = serializers.CharField(max_length=30)
    password = fields.PasswordField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        self.user = authenticate(email=email, password=password)

        if self.user and self.user.is_active:
            return UserSerializer(self.user).data
        else:
            msg = 'Unable to login with provided credentials.'
            raise serializers.ValidationError(msg)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializers used for User objects.
    """
    token = serializers.Field(source='token')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone',
                  'type', 'status', 'title', 'address_1', 'address_2',
                  'country', 'city', 'state', 'zip', 'facebook_url',
                  'twitter_url', 'google_url', 'gravatar_url', 'institution',
                  'department', 'description', 'logo', 'company_name', 'token')


class UserSimpleSerializer(DynamicFieldsModelSerializer):
    """
    Simple User serializer used to serialize model.
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone',
                  'type', 'status', 'title', 'address_1', 'address_2',
                  'country', 'city', 'state', 'zip', 'facebook_url',
                  'twitter_url', 'google_url', 'gravatar_url', 'institution',
                  'department', 'description', 'logo', 'company_name')
