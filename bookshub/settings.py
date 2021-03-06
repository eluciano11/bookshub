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
        'corsheaders',
        'django_filters',
        'djstripe',
        'storages',

        # Apps
        'bookshub.users',
        'bookshub.books',
        'bookshub.contact',
        'bookshub.report',
        'bookshub.offers',
        'bookshub.cart',
    )

    MIDDLEWARE_CLASSES = (
        'djangosecure.middleware.SecurityMiddleware',
        'corsheaders.middleware.CorsMiddleware',
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
        'djstripe.context_processors.djstripe_settings',
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

    EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

    DEFAULT_FROM_EMAIL = values.Value()
    EMAIL_HOST = values.Value()
    EMAIL_HOST_USER = values.Value()
    EMAIL_HOST_PASSWORD = values.Value()
    EMAIL_PORT = values.IntegerValue()
    EMAIL_USE_TLS = values.BooleanValue(False)

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework.filters.DjangoFilterBackend',
        ),
        'EXCEPTION_HANDLER':
        'bookshub.utils.exceptions.custom_exception_handler',
        'PAGINATE_BY': 25,
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

    # CORS settings
    CORS_ORIGIN_ALLOW_ALL = True

    # Email
    BOOKSHUB_EMAIL = values.Value(environ_prefix=None)

    # ISBNDB API KEY
    ISBNDB_API_KEY = values.Value(environ_prefix=None)

    # Stripe Keys
    STRIPE_PUBLIC_KEY = values.Value(environ_prefix=None)
    STRIPE_SECRET_KEY = values.Value(environ_prefix=None)

    DJSTRIPE_PLANS = {
        "student": {
            "stripe_plan_id": "student_plan",
            "name": "Monthly Subscription $0",
            "description": "Place up to 10 unique books for sale.",
            "price": 0,
            "currency": "usd",
            "interval": "month"
        },
        "monthly_5": {
            "stripe_plan_id": "bronze_plan",
            "name": "Monthly Subscription $5",
            "description": "Place up to 20 unique books for sale.",
            "price": 500,
            "currency": "usd",
            "interval": "month"
        },
        "monthly_10": {
            "stripe_plan_id": "silver_plan",
            "name": "Monthly Subscription $10",
            "description": "Place up to 20 unique books for sale.",
            "price": 1000,
            "currency": "usd",
            "interval": "month"
        },
        "monthly_20": {
            "stripe_plan_id": "gold_plan",
            "name": "Monthly Subscription $20",
            "description": "Place up to 20 unique books for sale.",
            "price": 2000,
            "currency": "usd",
            "interval": "month"
        },
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
        "api_version": '0.3',
        "enabled_methods": [
            'get',
            'post',
            'put',
            'patch',
            'delete'
        ],
        "is_authenticated": False,
        "is_superuser": False,
    }

    PROTOCOL = 'http'

    # Django Debug Toolbar
    DEBUG_TOOLBAR_PATCH_SETTINGS = values.BooleanValue(
        environ_prefix=None, default=False)

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

    # django-secure settings
    PROTOCOL = 'https'
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_FRAME_DENY = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    STATIC_URL = 'https://bookshub.s3.amazonaws.com/'
    MEDIA_URL = STATIC_URL

    AWS_PRELOAD_METADATA = True
    AWS_QUERYSTRING_AUTH = False
    AWS_ACCESS_KEY_ID = values.Value(environ_prefix=None)
    AWS_SECRET_ACCESS_KEY = values.Value(environ_prefix=None)
    AWS_STORAGE_BUCKET_NAME = values.Value(environ_prefix=None)
