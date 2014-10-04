import os
import datetime

from configurations import Configuration, values


class Common(Configuration):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    ENVIRONMENT = values.Value(environ_prefix=None, default='DEVELOPMENT')

    SECRET_KEY = values.SecretValue(environ_prefix=None)

    DEBUG = values.BooleanValue(False)

    TEMPLATE_DEBUG = values.BooleanValue(DEBUG)

    ALLOWED_HOSTS = ['*']

    # Application definition

    INSTALLED_APPS = (
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
        'djrill',
        'taggit',
        'djangosecure',

        # Apps
        'bookshub.users',
        'bookshub.books',
    )

    MIDDLEWARE_CLASSES = (
        'djangosecure.middleware.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

    # STATICFILES_DIRS = (
    #     os.path.join(BASE_DIR, 'static'),
    # )

    # TEMPLATE_DIRS = (
    #     os.path.join(BASE_DIR, 'templates'),
    # )

    SITE_ID = 1

    MANDRILL_API_KEY = values.Value(environ_prefix=None)

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
            'bookshub.users.authentication.JWTAuthentication',
            'bookshub.users.authentication.SessionAuthentication',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'EXCEPTION_HANDLER':
        'bookshub.utils.exceptions.custom_exception_handler',
    }

    JWT_AUTH = {
        'JWT_PAYLOAD_HANDLER':
        'bookshub.utils.jwt_handlers.jwt_payload_handler',
        'JWT_EXPIRATION_DELTA': datetime.timedelta(days=200),
        'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=201),
        'JWT_ALLOW_REFRESH': True,
    }

    AUTH_USER_MODEL = 'users.User'

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
            }
        }
    }

    ENCRYPTED_FIELDS_KEYDIR = 'fieldkeys'
    # ENCRYPTED_FIELDS_KEYDIR = 'fieldkeys'


class Development(Common):

    DEBUG = True

    TEMPLATE_DEBUG = DEBUG

    DEBUG_TOOLBAR_PATCH_SETTINGS = values.BooleanValue(False)

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


class Testing(Development):
    LOGGING_CONFIG = None

    # Database Settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(Common.BASE_DIR, 'testing_db.sqlite3'),
        }
    }

    # Password Hashers
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    # South
    SOUTH_TESTS_MIGRATE = False

    # Debug Toolbar
    DEBUG_TOOLBAR_PATCH_SETTINGS = False


class Production(Common):
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

    # django-secure settings
    PROTOCOL = 'https'
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_FRAME_DENY = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
