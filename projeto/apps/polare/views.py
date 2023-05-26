import django_filters
from django.contrib.auth import mixins
from django.views import generic

from projeto.apps.arquitetura.filters import QueryParamFilterSet
from projeto.apps.arquitetura.views import ElidedListView
from projeto.apps.polare.models import Entrega, PlanoIndividual, Subtarefa

from . import models


class HomeView(mixins.LoginRequiredMixin, generic.TemplateView):

    template_name = 'polare/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        planos_2022 = PlanoIndividual.objects.filter(ano_referencia=2022, ativo=True)
        planos_2023 = PlanoIndividual.objects.filter(ano_referencia=2023, ativo=True)
        ctx['total_planos_2022'] = planos_2022.count()
        ctx['total_planos_2023'] = planos_2023.count()

        ctx['total_entregas_2022'] = Entrega.objects.filter(
            plano_individual__ano_referencia=2022, plano_individual__ativo=True
        ).distinct().count()
        ctx['total_entregas_2023'] = Entrega.objects.filter(
            plano_individual__ano_referencia=2023, plano_individual__ativo=True
        ).distinct().count()

        ctx['total_subtarefas_2022'] = Subtarefa.objects.filter(
            entrega__plano_individual__ano_referencia=2022, entrega__plano_individual__ativo=True
        ).distinct().count()
        ctx['total_subtarefas_2023'] = Subtarefa.objects.filter(
            entrega__plano_individual__ano_referencia=2023, entrega__plano_individual__ativo=True
        ).distinct().count()
        return ctx


home = HomeView.as_view()


class PlanoIndividualFilter(QueryParamFilterSet):

    nome = django_filters.CharFilter(label='Nome', lookup_expr='icontains')
    siape = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = models.PlanoIndividual
        fields = ['nome', 'siape']


class QuantitativoGeral(ElidedListView):

    template_name = 'polare/relatorios/quantitativo_geral.html'
    model = models.PlanoIndividual
    queryset = models.PlanoIndividual.objects.planos_para_api()
    context_object_name = 'planos'
    paginate_by = 5
    page_kwarg = 'pagina'
    ordering = ['nome', 'ano_referencia']
    filter_class = PlanoIndividualFilter


quantitativo_geral = QuantitativoGeral.as_view()
