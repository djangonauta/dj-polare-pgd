from rest_framework import permissions, viewsets

from . import models, serializers


class PlanoIndividualViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.PlanoIndividualSerializer
    queryset = (models.PlanoIndividual.objects
                .prefetch_related('entregas__subtarefas', 'entregas__atividade', 'horarios').all())
