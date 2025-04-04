from django.db import models


class PlanoIndividualManager(models.Manager):

    def planos_para_api(self):
        campos = ('entregas__subtarefas', 'entregas__atividade', 'horarios')
        return self.filter().select_related('unidade_localizacao').prefetch_related(*campos).all()
