# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa: F405

# Django Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']  # noqa: F405
INTERNAL_IPS = ['127.0.0.1']

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE  # noqa: F405

MEDIA_ROOT = BASE_DIR / 'downloads-test'  # noqa: F405
