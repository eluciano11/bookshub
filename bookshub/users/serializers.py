from django.utils.encoding import smart_str
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User
from ..utils.serializers import DynamicFieldsModelSerializer
from ..utils import fields


class SigninSerializer(serializers.Serializer):
    """
    Serializer that handles signin endpoint data.
    """
    email = serializers.EmailField(max_length=30)
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


class SignupSerializer(serializers.Serializer):
    """
    Serializers used to create a user.
    """

    email = serializers.EmailField(max_length=30)
    password = serializers.CharField(max_length=30, write_only=True)
    username = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=16)
    type = serializers.CharField(max_length=20)
    status = serializers.CharField(max_length=20)
    title = serializers.CharField(max_length=30)

    def validate_email(self, attrs, source):
        email = attrs[source].lower().strip()

        is_found = User.objects.filter(email__icontains=email)

        if is_found:
            message = 'Email already in use'
            raise serializers.ValidationError(message)

        return attrs

    def validate_username(self, attrs, source):
        username = attrs[source].lower().strip()

        print username

        is_found = User.objects.filter(username=username).exists()

        if is_found:
            message = 'Username already in use'
            raise serializers.ValidationError(message)

        return attrs

    def validate_password(self, attrs, source):
        password = attrs[source]

        if password:
            attrs['password'] = smart_str(password)

        return attrs

    def create_user(self, attrs):
        username = attrs['username']
        email = attrs['email']
        password = attrs['password']
        first_name = attrs['first_name']
        last_name = attrs['last_name']
        phone = attrs['phone']
        type = attrs['type']
        status = attrs['status']
        title = attrs['title']

        user = User.objects.create_user(
            username, email, first_name, last_name,
            phone, type, title, password)
        user.status = status
        user.save()

        return user

    def validate(self, attrs):
        user = self.create_user(attrs)
        return UserSerializer(user).data


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password = fields.PasswordField(write_only=True)
    new_password_confirmation = fields.PasswordField(write_only=True)

    class Meta:
        model = User
        fields = ('current_password', 'new_password', 'new_password_confirmation',)

    def validate_current_password(self, attrs, source):
        current_password = attrs[source]
        user = self.object

        #and not user.check_password(current_password)
        if user and False:
            message = 'Current password is invalid'
            raise serializers.ValidationError(message)

        return attrs

    def validate_new_password_confirmation(self, attrs, source):
        confirmation = attrs[source]
        new_password = attrs['new_password']

        if confirmation != new_password:
            message = 'The passwords are not the same'
            raise serializers.ValidationError(message)

        return attrs

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.change_password(attrs.get('new_password_confirmation'))
            return instance

        return User()
