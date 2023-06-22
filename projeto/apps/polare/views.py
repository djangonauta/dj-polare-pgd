import django_filters
import view_breadcrumbs
from django import urls
from django.contrib.auth import mixins
from django.db.models import Count
from django.utils import functional
from django.views import generic

from projeto.apps.arquitetura.filters import QueryParamFilterSet
from projeto.apps.arquitetura.views import ElidedListView
from projeto.apps.polare.models import Entrega, PlanoIndividual, Subtarefa

from . import models


class HomeView(mixins.LoginRequiredMixin, view_breadcrumbs.BaseBreadcrumbMixin, generic.TemplateView):

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
        model = models.PlanoIndividual
        fields = ['nome', 'siape']


class QuantitativoGeral(view_breadcrumbs.ListBreadcrumbMixin, ElidedListView):

    template_name = 'polare/relatorios/quantitativo_geral.html'
    model = models.PlanoIndividual
    queryset = models.PlanoIndividual.objects.planos_para_api()
    context_object_name = 'planos'
    paginate_by = 5
    page_kwarg = 'pagina'
    ordering = ['nome', 'ano_referencia']
    filter_class = PlanoIndividualFilter

    @functional.cached_property
    def crumbs(self):
        return [('Quantitativo Geral', urls.reverse('polare:quantitativo_geral'))]


quantitativo_geral = QuantitativoGeral.as_view()


class QuantitativoDetalhe(view_breadcrumbs.DetailBreadcrumbMixin, generic.DetailView):

    template_name = 'polare/relatorios/quantitativo_detalhe.html'
    model = models.PlanoIndividual
    context_object_name = 'plano'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        queryset = PlanoIndividual.objects.get(pk=self.kwargs['pk']).entregas.prefetch_related('subtarefas')
        queryset = queryset.annotate(totalsub=Count('subtarefas'))
        dados = {}
        ids = []
        for p in queryset:
            dados.setdefault(p.intervalo, []).append(p.totalsub)
            ids.append(p.pk)

        data = []
        for k, v in dados.items():
            data.append([f'{len(v)} entrega(s)\n{k}', sum(v)])

        ctx['data'] = data
        return ctx

    @functional.cached_property
    def crumbs(self):
        pk = self.kwargs['pk']
        return [('Quantitativo Detalhe', urls.reverse('polare:quantitativo_detalhe', args=[pk]))]


quantitativo_detalhe = QuantitativoDetalhe.as_view()


class EntregaDetalhe(generic.DetailView):

    template_name = 'polare/entregas/entrega_detalhe.html'
    model = models.Entrega
    context_object_name = 'entrega'


entrega_detalhe = EntregaDetalhe.as_view()
