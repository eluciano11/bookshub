from django.utils.encoding import smart_str
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User
from ..utils.serializers import DynamicFieldsModelSerializer
from ..utils import fields
from ..utils.validators import is_valid_email


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
    email = serializers.EmailField(max_length=254)
    password = fields.PasswordField(write_only=True)
    username = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    phone = serializers.CharField(max_length=16)
    type = serializers.CharField(max_length=20)
    title = serializers.CharField(max_length=30)

    def validate_email(self, attrs, source):
        email = attrs[source].lower().strip()

        is_found = User.objects.filter(email__iexact=email)

        if is_found:
            message = 'Email already in use'
            raise serializers.ValidationError(message)

        return attrs

    def validate_username(self, attrs, source):
        username = attrs[source].lower().strip()

        is_found = User.objects.filter(username__iexact=username)

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
        status = 'normal'
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
        fields = ('current_password', 'new_password',
                  'new_password_confirmation')

    def validate_current_password(self, attrs, source):
        current_password = attrs[source]
        user = self.object

        if user and not user.check_password(current_password):
            message = 'Current password is invalid'
            raise serializers.ValidationError(message)

        return attrs

    def validate_new_password_confirmation(self, attrs, source):
        confirmation = attrs[source]
        new_password = attrs['new_password']

        if confirmation != new_password:
            message = 'The passwords are not the same'
            raise serializers.ValidationError(message)

        attrs[source] = smart_str(confirmation)

        return attrs

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.change_password(attrs.get('new_password_confirmation'))
            return instance

        return User()


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer that handles forgot password endpoint.
    """
    email = serializers.EmailField(max_length=254)

    def validate_email(self, attrs, source):
        email = attrs[source].lower()

        try:
            self.user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            msg = 'No user found.'
            raise serializers.ValidationError(msg)

        return attrs

    def send_password_reset_email(self):
        self.user.send_password_reset_email()


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer that handles reset password endpoint.
    """
    token = serializers.CharField(write_only=True)
    new_password = fields.PasswordField(write_only=True)

    def validate_new_password(self, attrs, source):
        new_password = attrs[source]

        if new_password:
            attrs['new_password'] = smart_str(new_password)

        return attrs

    def validate_token(self, attrs, source):
        token = attrs[source]

        self.user = User.objects.get_from_password_reset_token(token)

        if not self.user:
            msg = 'Invalid password reset token.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate(self, attrs):
        self.user.change_password(attrs['new_password'])

        return {
            'password_reset': True
        }


class CancelAccountSerializer(serializers.ModelSerializer):
    """
    Serializer that handles cancel account in user settings endpoint.
    """
    current_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('current_password', )

    def validate_current_password(self, attrs, source):
        password = attrs[source]
        user = self.object

        if user and not user.check_password(password):
            message = 'Current password is invalid'
            raise serializers.ValidationError(message)

        return attrs

    def save_object(self, obj, **kwargs):
        obj.is_active = False
        super(CancelAccountSerializer, self).save_object(obj, **kwargs)


class UserSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer that handles user settings endpoint.
    """
    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=30)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    token = serializers.Field(source='token')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone',
          'type', 'status', 'title', 'address_1', 'address_2',
          'country', 'city', 'state', 'zip', 'facebook_url',
          'twitter_url', 'google_url', 'gravatar_url', 'institution',
          'department', 'description', 'logo', 'company_name')

    def save_object(self, obj, **kwargs):
        super(UserSettingsSerializer, self).save_object(obj, **kwargs)
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone',
                  'type', 'status', 'title', 'address_1', 'address_2',
                  'country', 'city', 'state', 'zip', 'facebook_url',
                  'twitter_url', 'google_url', 'gravatar_url', 'institution',
                  'department', 'description', 'logo', 'company_name', 'token')

    def validate_email(self, attrs, source):
        if not source in attrs:
            return attrs
        
        email = attrs[source].lower()
        user = self.object

        users = User.objects.filter(
            email__iexact=email).exclude(pk=user.id)

        if users.exists():
            msg = 'Email already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate_username(self, attrs, source):
        if not source in attrs:
            return attrs

        username = attrs[source].lower()
        attrs[source] = username
        user = self.object

        if is_valid_email(username):
            msg = 'Invalid username.'
            raise serializers.ValidationError(msg)

        users = User.objects.filter(
            username=username).exclude(pk=user.id)

        if users.exists():
            msg = 'Username already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def save_object(self, obj, **kwargs):
        super(UserSettingsSerializer, self).save_object(obj, **kwargs)
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone',
                  'type', 'status', 'title', 'address_1', 'address_2',
                  'country', 'city', 'state', 'zip', 'facebook_url',
                  'twitter_url', 'google_url', 'gravatar_url', 'institution',
                  'department', 'description', 'logo', 'company_name', 'token')

    def validate_email(self, attrs, source):
        if not source in attrs:
            return attrs
        
        email = attrs[source].lower()
        user = self.object

        users = User.objects.filter(
            email__iexact=email).exclude(pk=user.id)

        if users.exists():
            msg = 'Email already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate_username(self, attrs, source):
        if not source in attrs:
            return attrs

        username = attrs[source].lower()
        attrs[source] = username
        user = self.object

        if is_valid_email(username):
            msg = 'Invalid username.'
            raise serializers.ValidationError(msg)

        users = User.objects.filter(
            username=username).exclude(pk=user.id)

        if users.exists():
            msg = 'Username already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def save_object(self, obj, **kwargs):
        super(UserSettingsSerializer, self).save_object(obj, **kwargs)
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone',
                  'type', 'status', 'title', 'address_1', 'address_2',
                  'country', 'city', 'state', 'zip', 'facebook_url',
                  'twitter_url', 'google_url', 'gravatar_url', 'institution',
                  'department', 'description', 'logo', 'company_name', 'token')

    def validate_email(self, attrs, source):
        if not source in attrs:
            return attrs
        
        email = attrs[source].lower()
        user = self.object

        users = User.objects.filter(
            email__iexact=email).exclude(pk=user.id)

        if users.exists():
            msg = 'Email already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate_username(self, attrs, source):
        if not source in attrs:
            return attrs

        username = attrs[source].lower()
        attrs[source] = username
        user = self.object

        if is_valid_email(username):
            msg = 'Invalid username.'
            raise serializers.ValidationError(msg)

        users = User.objects.filter(
            username=username).exclude(pk=user.id)

        if users.exists():
            msg = 'Username already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def save_object(self, obj, **kwargs):
        super(UserSettingsSerializer, self).save_object(obj, **kwargs)
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone',
                  'type', 'status', 'title', 'address_1', 'address_2',
                  'country', 'city', 'state', 'zip', 'facebook_url',
                  'twitter_url', 'google_url', 'gravatar_url', 'institution',
                  'department', 'description', 'logo', 'company_name', 'token')

    def validate_email(self, attrs, source):
        if not source in attrs:
            return attrs
        
        email = attrs[source].lower()
        user = self.object

        users = User.objects.filter(
            email__iexact=email).exclude(pk=user.id)

        if users.exists():
            msg = 'Email already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def validate_username(self, attrs, source):
        if not source in attrs:
            return attrs

        username = attrs[source].lower()
        attrs[source] = username
        user = self.object

        if is_valid_email(username):
            msg = 'Invalid username.'
            raise serializers.ValidationError(msg)

        users = User.objects.filter(
            username=username).exclude(pk=user.id)

        if users.exists():
            msg = 'Username already exists.'
            raise serializers.ValidationError(msg)

        return attrs

    def save_object(self, obj, **kwargs):
        super(UserSettingsSerializer, self).save_object(obj, **kwargs)
