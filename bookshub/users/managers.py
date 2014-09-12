import jwt

from django.conf import settings
from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    def get_from_password_reset_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            return None

        payload_type = payload.get('type')
        user_id = payload.get('id')
        user_token = payload.get('token_version')

        if payload_type == 'PasswordReset' and user_id and user_token:
            try:
                return self.get(pk=user_id, token_version=user_token)
            except self.model.DoesNotExist:
                pass

        return None

    def create_user(self, username, email, first_name, last_name, phone,
                    type, title, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            type=type,
            title=title
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name,
                         phone, type, title, password):
        user = self.create_user(
            username,
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            type=type,
            title=title,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class ActiveAccountManager(AccountManager):
    def get_queryset(self):
        queryset = super(ActiveAccountManager, self).get_queryset()
        return queryset.filter(is_active=True)
