import pathlib

import environ
from django import urls
from django.conf import global_settings

env = environ.Env()
environ.Env.read_env()

# ADMINS = 'Fulano=fulano@email.com,Beltrano=beltrano@email.com'
admins = env.dict('ADMINS')
ADMINS = admins.items()
MANAGERS = env.dict('MANAGERS', default=admins).items()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {'default': env.db()}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# Email
# https://docs.djangoproject.com/en/dev/topics/email/
env.EMAIL_SCHEMES.update(postoffice='post_office.EmailBackend')
vars().update(env.email_url())

# default charset in django.core.email.
DEFAULT_CHARSET = env('DEFAULT_CHARSET', default='utf-8')
# default from_email in EmailMessage.
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='webmaster@localhost')
# default prefix + subject in mail_admins/managers.
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', default='[Django]')
# default from: header in mail_admins/managers.
SERVER_EMAIL = env('SERVER_EMAIL', default='admin@localhost')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'auditlog',
    'django_celery_beat',
    'django_celery_results',
    'django_extensions',
    'hijack',
    'hijack.contrib.admin',
    'post_office',
    'rest_framework',
    'view_breadcrumbs',
    'widget_tweaks',
]

PROJECT_APPS = [
    'projeto.apps.administrativo',
    'projeto.apps.administrativo.usuarios',
    'projeto.apps.arquitetura',
    'projeto.apps.polare',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hijack.middleware.HijackUserMiddleware',
]

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'projeto' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ROOT_URLCONF = 'projeto.urls'

WSGI_APPLICATION = 'projeto.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = '/public/'
STATIC_ROOT = BASE_DIR / 'public'
STATICFILES_DIRS = [BASE_DIR / 'projeto' / 'assets']
BREADCRUMBS_TEMPLATE = '_includes/breadcrumbs.html'

MEDIA_URL = '/downloads/'
MEDIA_ROOT = BASE_DIR / 'downloads'

AUTH_USER_MODEL = 'usuarios.Usuario'
LOGIN_URL = urls.reverse_lazy('account_login')
LOGIN_REDIRECT_URL = urls.reverse_lazy('polare:home')

# https://django-allauth.readthedocs.io/en/latest/
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = env('ACCOUNT_EMAIL_VERIFICATION', default='none')  # 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = ''
if env('DISABLE_ACCOUNT_REGISTRATION', default=False):
    ACCOUNT_ADAPTER = 'projeto.apps.administrativo.usuarios.adapters.DisableSignupAdapter'
    REST_AUTH_REGISTER_SERIALIZERS = {
        'REGISTER_SERIALIZER': 'projeto.apps.administrativo.usuarios.serializers.DisableSignupSerializer'
    }

OLD_PASSWORD_FIELD_ENABLED = True

AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + \
    ['django_auth_ldap.backend.LDAPBackend',
     'allauth.account.auth_backends.AuthenticationBackend']

# https://django-auth-ldap.readthedocs.io/en/latest/
AUTH_LDAP_SERVER_URI = env('AUTH_LDAP_SERVER_URI', default='')
AUTH_LDAP_USER_DN_TEMPLATE = env('AUTH_LDAP_SERVER_URI', default='')

# https://docs.djangoproject.com/en/dev/topics/i18n/
LOCALE_PATHS = [BASE_DIR / 'projeto' / 'locale']

# https://docs.celeryq.dev/en/stable/userguide/configuration.html
CELERY_BROKER_URL = env('BROKER_URL')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# https://django-extensions.readthedocs.io/en/latest/graph_models.html
GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

# https://docs.djangoproject.com/en/dev/topics/cache/
env.CACHE_SCHEMES.update(redis='django.core.cache.backends.redis.RedisCache')
CACHES = {'default': env.cache_url()}
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',
                                'rest_framework.filters.SearchFilter',
                                'rest_framework.filters.OrderingFilter'),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DATETIME_FORMAT': '%Y-%m-%d',
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# PGD https://api-programadegestao.economia.gov.br/docs
API_PGD_LOGIN_URL = env('API_PGD_LOGIN_URL')
API_PGD_PLANO_TRABALHO_URL = env('API_PGD_PLANO_TRABALHO_URL')
API_PGD_CREDENCIAIS = env.dict('API_PGD_CREDENCIAIS')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
