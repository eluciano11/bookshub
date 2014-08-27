import os
import datetime

from configurations import Configuration, values


class Common(Configuration):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    ENVIRONMENT = values.Value(environ_prefix=None, default='DEVELOPMENT')

    SECRET_KEY = values.SecretValue(environ_prefix=None)

    DEBUG = values.BooleanValue(False)

    TEMPLATE_DEBUG = values.BooleanValue(DEBUG)

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = (
        'bootstrap_admin',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',

        # Third party
        'south',
        'rest_framework',
        'django_extensions',
        'reversion',
        'django_gravatar',
        'django_countries',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.twitter',

        # Apps
        'bookshub.accounts'

    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',
        # allauth specific context processors
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",
    )

    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",

        # `allauth` specific authentication methods, such as login by e-mail
        "allauth.account.auth_backends.AuthenticationBackend",
    )

    ROOT_URLCONF = 'bookshub.urls'

    WSGI_APPLICATION = 'bookshub.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

    DATABASES = values.DatabaseURLValue(
        'sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3')))

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/

    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'templates'),
    )

    SITE_ID = 1

    DEFAULT_FROM_EMAIL = values.Value()
    EMAIL_HOST = values.Value()
    EMAIL_HOST_USER = values.Value()
    EMAIL_HOST_PASSWORD = values.Value()
    EMAIL_PORT = values.IntegerValue()
    EMAIL_USE_TLS = values.BooleanValue(False)

    # Django REST framework
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
    }

    JWT_AUTH = {
        'JWT_PAYLOAD_HANDLER':
            'bookshub.utils.jwt_handlers.jwt_payload_handler',

        'JWT_EXPIRATION_DELTA': datetime.timedelta(days=90)
    }


class Development(Common):
    DEBUG = True

    TEMPLATE_DEBUG = DEBUG

    # Development-only installed apps
    Common.INSTALLED_APPS += (
        'debug_toolbar',
        'rest_framework_swagger',
    )

    SWAGGER_SETTINGS = {
        "exclude_namespaces": [],
        "api_version": '0.1',
        "api_path": "/",
        "enabled_methods": [
            'get',
            'post',
            'put',
            'patch',
            'delete'
        ],
        "api_key": '',
        "is_authenticated": False,
        "is_superuser": False,
    }

    PROTOCOL = 'http'

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Django Debug Toolbar
    DEBUG_TOOLBAR_PATCH_SETTINGS = values.BooleanValue(
        environ_prefix=None, default=True)

    # Dummy cache for development
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


class Production(Common):
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

    # django-secure settings
    PROTOCOL = 'https'
