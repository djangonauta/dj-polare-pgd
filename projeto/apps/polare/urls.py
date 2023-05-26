from django import urls

from . import views

app_name = 'polare'

urlpatterns = [
    urls.path('', views.home, name='home'),
    urls.path('relatorios/quantitativo/geral/', views.quantitativo_geral, name='quantitativo_geral'),
]
