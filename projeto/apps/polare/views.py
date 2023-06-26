import django_filters
from django import urls
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils import functional
from django.views.generic import DetailView, TemplateView
from view_breadcrumbs import BaseBreadcrumbMixin, DetailBreadcrumbMixin, ListBreadcrumbMixin

from projeto.apps.arquitetura.filters import QueryParamFilterSet
from projeto.apps.arquitetura.views import ElidedListView

from .models import Entrega, PlanoIndividual, Subtarefa


class HomeView(LoginRequiredMixin, BaseBreadcrumbMixin, TemplateView):

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

    @functional.cached_property
    def crumbs(self):
        return [('Home', urls.reverse('polare:home'))]


home = HomeView.as_view()


class PlanoIndividualFilter(QueryParamFilterSet):

    nome = django_filters.CharFilter(label='Nome', lookup_expr='istartswith')
    siape = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = PlanoIndividual
        fields = ['nome', 'siape']


class QuantitativoGeral(LoginRequiredMixin, ListBreadcrumbMixin, ElidedListView):

    template_name = 'polare/relatorios/quantitativo_geral.html'
    model = PlanoIndividual
    queryset = PlanoIndividual.objects.planos_para_api()
    context_object_name = 'planos'
    paginate_by = 5
    page_kwarg = 'pagina'
    ordering = ['nome', 'ano_referencia']
    filter_class = PlanoIndividualFilter

    @functional.cached_property
    def crumbs(self):
        return [('Quantitativo Geral', urls.reverse('polare:quantitativo_geral'))]


quantitativo_geral = QuantitativoGeral.as_view()


class QuantitativoDetalhe(LoginRequiredMixin, DetailBreadcrumbMixin, DetailView):

    template_name = 'polare/relatorios/quantitativo_detalhe.html'
    model = PlanoIndividual
    context_object_name = 'plano'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        queryset = PlanoIndividual.objects.get(pk=self.kwargs['pk']).entregas.prefetch_related('subtarefas')
        queryset = queryset.annotate(totalsub=Count('subtarefas'))
        dados: dict[str, list] = {}
        for entrega in queryset:
            dados.setdefault(entrega.intervalo, []).append(entrega.totalsub)

        data = []
        for intervalo, lista_totalsub in dados.items():
            data.append([f'{len(lista_totalsub)} entrega(s)\n{intervalo}', sum(lista_totalsub)])

        ctx['data'] = data
        return ctx

    @functional.cached_property
    def crumbs(self):
        return [
            ('Quantitativo Geral', urls.reverse('polare:quantitativo_geral')),
            ('Quantitativo Detalhe', urls.reverse('polare:quantitativo_detalhe', args=[self.kwargs['pk']])),
        ]


quantitativo_detalhe = QuantitativoDetalhe.as_view()


class EntregaDetalhe(DetailView):

    template_name = 'polare/entregas/entrega_detalhe.html'
    model = Entrega
    context_object_name = 'entrega'


entrega_detalhe = EntregaDetalhe.as_view()
