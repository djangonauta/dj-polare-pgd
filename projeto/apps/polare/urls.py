from django import urls

from . import views

app_name = 'polare'

urlpatterns = [
    urls.path('', views.home, name='home'),
    urls.path('relatorios/quantitativo/geral/', views.quantitativo_geral, name='quantitativo_geral'),
    urls.path('relatorios/quantitativo/geral/<int:pk>/', views.quantitativo_detalhe, name='quantitativo_detalhe'),  # noqa: E501
]
