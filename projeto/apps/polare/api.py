from rest_framework import permissions, viewsets

from . import models, serializers


class PlanoIndividualViewSet(viewsets.ReadOnlyModelViewSet):
    """Lista de Planos Individuais ativos no sistema Polare"""

    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.PlanoIndividualSerializer
    queryset = models.PlanoIndividual.objects.planos_para_api()
    search_fields = ('nome', 'siape', 'modelo_trabalho')

    def get_view_name(self):
        return 'Listagem de Planos Individuais'


class PlanoIndividualPROGEPViewSet(PlanoIndividualViewSet):

    serializer_class = serializers.PlanoIndividualPROGEPSerializer
