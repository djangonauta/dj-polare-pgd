from django.contrib.auth import mixins
from django.views import generic

from projeto.apps.polare.models import PlanoIndividual, Entrega, Subtarefa


class AppView(mixins.LoginRequiredMixin, generic.TemplateView):

    template_name = 'app.html'

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


app = AppView.as_view()
