import time
import uuid
import jwt
from calendar import timegm
from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.sites.models import Site

from django_countries.fields import CountryField
from django_gravatar.helpers import get_gravatar_url
from rest_framework_jwt.settings import api_settings

from ..utils.models import BaseModel
from ..utils.jwt_handlers import jwt_payload_handler, jwt_encode_handler
from .constants import ACCOUNT_TYPE_CHOICES, ACCOUNT_STATUS_CHOICES
from .managers import AccountManager, ActiveAccountManager


def get_logo_path(filename):
    return "logos/%s_%s" % \
           (str(time()).replace('.', '_'), filename)


class User(BaseModel, AbstractBaseUser):
    # Help text

    username_help_text = """Required. 30 characters or fewer.
                           Letters, numbers and
                           @/./+/-/_ characters"""

    is_staff_help_text = """Designates whether the user
                            can log into this admin site."""

    is_active_help_text = """Designates whether this user should be treated as
                            active. Unselect this instead of deleting users."""

    is_superuser_help_text = """Designates that this user has all
                               permissions without explicitly
                               assigning them."""

    email = models.EmailField('email address', max_length=254, unique=True)
    username = models.CharField(
        max_length=30, help_text=username_help_text,
        unique=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=16, blank=True)
    type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    status = models.CharField(
        max_length=20, choices=ACCOUNT_STATUS_CHOICES,
        default='normal')
    title = models.CharField(max_length=30, blank=True)

    address_1 = models.CharField(max_length=100, blank=True)
    address_2 = models.CharField(max_length=100, blank=True)
    country = CountryField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip = models.CharField(max_length=15, blank=True)

    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    google_url = models.URLField(blank=True)
    gravatar_url = models.URLField(blank=True)

    institution = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=140, blank=True)
    logo = models.ImageField(
        upload_to=get_logo_path, height_field=100,
        width_field=100, blank=True)
    company_name = models.CharField(max_length=50, blank=True)

    is_staff = models.BooleanField(default=False, help_text=is_staff_help_text)
    is_superuser = models.BooleanField(
        default=False, help_text=is_superuser_help_text)
    is_active = models.BooleanField(default=True, help_text=is_active_help_text)

    token_version = models.CharField(
        max_length=36, default=str(uuid.uuid4()), unique=True, db_index=True)

    objects = AccountManager()
    active = ActiveAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name',
                       'phone', 'type', 'title']

    def __str__(self):
        return self.email

    def is_admin(self):
        return self.is_superuser

    def save(self, *args, **kwargs):
        if not self.pk or self.has_field_changed('email'):
            self.gravatar_url = get_gravatar_url(self.email)

        return super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        """
        Returns True if user is an active superuser.
        """
        if self.is_active and self.is_superuser:
            return True

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms
        for this object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if user is an active superuser.
        """
        if self.is_active and self.is_superuser:
            return True

    @property
    def token(self):
        """
        Returns a JSON Web Token used for Authentication.
        """
        payload = jwt_payload_handler(self)
        if api_settings.JWT_ALLOW_REFRESH:
            payload['orig_iat'] = timegm(
                datetime.utcnow().utctimetuple()
            )
        return jwt_encode_handler(payload)

    @property
    def password_reset_token(self):
        """
        Returns a JSON Web Token used for Password Reset
        """
        payload = {
            'type': 'PasswordReset',
            'id': self.pk,
            'token_version': self.token,
        }

        jwt_token = jwt.encode(payload, settings.SECRET_KEY)

        return jwt_token.decode('utf-8')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip() or self.username

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name or self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def set_password(self, raw_password):
        """
        Sets the user's password and changes token_version.
        """
        super(User, self).set_password(raw_password)
        self.reset_token_version()

    def change_password(self, raw_password):
        """
        Sets the user's password, changes token_version, and notifies user.
        """
        self.set_password(raw_password)
        self.reset_token_version()
        self.save()

        # TODO: send notification email - not sure if needed

    def reset_token_version(self):
        """
        Resets the user's token_version.
        """
        self.token_version = str(uuid.uuid4())

    def send_password_reset_email(self):
        self.email_user(
            "Reset Password",
            # TODO: use template instead of hard coded python
            "%s/reset_password_url_here/?token=%s"
            % (Site.objects.get_current(), self.password_reset_token),
            "robot@bookshub.com"
        )
