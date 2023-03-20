from django import urls
from django.conf import settings
from django.conf.urls import static
from django.contrib import admin
from django.views import generic

from . import api

urlpatterns = [
    urls.path('', generic.RedirectView.as_view(url='/api/v1/', permanent=True)),
    urls.path('api/v1/', api.urls),
    urls.path('api-auth/', urls.include('rest_framework.urls', namespace='rest_framework')),
    urls.path('admin/', admin.site.urls),
]

# media files in development
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [urls.path('__debug__/', urls.include('debug_toolbar.urls'))]
