import os

from django.core import wsgi
from projeto.whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projeto.settings.whitenoise")
application = WhiteNoise(wsgi.get_wsgi_application())
