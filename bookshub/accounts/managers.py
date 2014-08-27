import jwt

from django.conf import settings
from django.contrib.auth.models import UserManager as SimpleUserManager
from django.utils import timezone


class AccountManager(SimpleUserManager):
    def get_from_password_reset_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            return None

        payload_type = payload.get('type')
        account_id = payload.get('id')
        account_token = payload.get('token')

        if payload_type == 'PasswordReset' and account_id and account_token:
            try:
                return self.get(pk=account_id, token_version=account_token)
            except self.model.DoesNotExist:
                pass

        return None

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        account = self.model(email=email,
                             is_staff=is_staff, is_active=True,
                             is_superuser=is_superuser, last_login=now,
                             **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account


class ActiveAccountManager(AccountManager):
    def get_queryset(self):
        queryset = super(ActiveAccountManager, self).get_queryset()
        return queryset.filter(is_active=True)