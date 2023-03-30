from datetime import datetime

import arrow
from django.db import models

from . import managers


class Unidade(models.Model):

    id = models.BigIntegerField(primary_key=True)
    ativo = models.BooleanField()
    versao = models.BigIntegerField()
    codigo = models.CharField(max_length=255)
    hierarquia_organizacional = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    nome_ascii = models.CharField(max_length=255)
    sigla = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'polare\".\"unidade'


class PlanoIndividual(models.Model):

    id = models.BigIntegerField(primary_key=True)
    ativo = models.BooleanField()
    versao = models.BigIntegerField()
    ano_referencia = models.IntegerField()
    carga_horaria = models.IntegerField(blank=True, null=True)
    equipe = models.CharField(max_length=255, blank=True, null=True)
    modelo_trabalho = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    siape = models.CharField(max_length=255)
    situacao = models.CharField(max_length=255)

    unidade_localizacao = models.ForeignKey(
        Unidade,
        related_name='planos_individuais',
        on_delete=models.DO_NOTHING,
        db_column='id_unidade_localizacao',
    )
    unidade_lotacao = models.ForeignKey(
        Unidade,
        on_delete=models.DO_NOTHING,
        db_column='id_unidade_lotacao'
    )

    objects = managers.PlanoIndividualManager()

    class Meta:
        managed = False
        ordering = ('id',)
        db_table = 'polare\".\"plano_individual'

    @property
    def modelo_trabalho_numero(self):
        match self.modelo_trabalho:
            case 'PRESENCIAL': return 1
            case 'HIBRIDO': return 2
            case 'REMOTO': return 3
            case _: return 0

    @property
    def carga_horaria_total(self):
        formato = '%Y-%m-%d'
        inicio = datetime.strptime('2022-12-12', formato)
        fim = datetime.strptime('2023-05-12', formato)

        num_semanas = sum(1 for _ in arrow.Arrow.span_range('week', inicio, fim)) - 1
        return num_semanas * self.carga_horaria


class HorarioTrabalho(models.Model):

    id = models.BigIntegerField(primary_key=True)
    ativo = models.BooleanField()
    versao = models.BigIntegerField()
    horario_fim = models.CharField(max_length=255)
    horario_inicio = models.CharField(max_length=255)

    domingo = models.BooleanField(blank=True, null=True)
    segunda = models.BooleanField(blank=True, null=True)
    terca = models.BooleanField(blank=True, null=True)
    quarta = models.BooleanField(blank=True, null=True)
    quinta = models.BooleanField(blank=True, null=True)
    sexta = models.BooleanField(blank=True, null=True)
    sabado = models.BooleanField(blank=True, null=True)

    tipo_horario_trabalho = models.CharField(max_length=255, blank=True, null=True)

    plano_individual = models.ForeignKey(PlanoIndividual, models.DO_NOTHING, related_name='horarios')

    class Meta:
        managed = False
        db_table = 'polare\".\"horario_trabalho'


class Atividade(models.Model):

    id = models.BigIntegerField(primary_key=True)
    ativo = models.BooleanField()
    versao = models.BigIntegerField()
    complexidade_atividade = models.CharField(max_length=255)
    titulo = models.TextField()

    class Meta:
        managed = False
        db_table = 'polare\".\"atividade'


class Entrega(models.Model):

    id = models.BigIntegerField(primary_key=True)
    ativo = models.BooleanField()
    versao = models.BigIntegerField()
    titulo = models.TextField()
    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    tipo_entrega = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    atividade = models.ForeignKey(Atividade, related_name='entregas', on_delete=models.DO_NOTHING,
                                  blank=True, null=True)
    plano_individual = models.ForeignKey(PlanoIndividual, related_name='entregas',
                                         on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'polare\".\"entrega'

    def carga_horaria_tipo(self, tipo):
        formato = '%H:%M'
        horas = 0
        for horario in self.plano_individual.horarios.filter(ativo=True).all():
            dias = (horario.domingo, horario.segunda, horario.terca, horario.quarta, horario.quinta,
                    horario.sexta, horario.sabado)

            for dia in dias:
                if dia and horario.tipo_horario_trabalho.lower() == tipo:
                    fim = datetime.strptime(horario.horario_fim, formato)
                    inicio = datetime.strptime(horario.horario_inicio, formato)
                    delta = (fim - inicio)
                    horas += delta.days * 24 + delta.seconds / 3600

        return horas

    @property
    def tempo_presencial_estimado(self):
        return self.carga_horaria_tipo('presencial')

    @property
    def tempo_presencial_programado(self):
        return self.carga_horaria_tipo('presencial')

    @property
    def tempo_teletrabalho_estimado(self):
        return self.carga_horaria_tipo('remoto')

    @property
    def tempo_teletrabalho_programado(self):
        return self.carga_horaria_tipo('remoto')


class Subtarefa(models.Model):

    id = models.BigIntegerField(primary_key=True)
    ativo = models.BooleanField()
    versao = models.BigIntegerField()
    descricao = models.TextField()
    finalizado = models.BooleanField()
    entrega = models.ForeignKey(Entrega, related_name='subtarefas', on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'polare\".\"subtarefa'

    def finalizado_texto(self):
        return 'Sim' if self.finalizado else 'Não'