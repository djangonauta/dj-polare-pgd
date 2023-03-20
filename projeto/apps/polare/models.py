from django.db import models


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

    class Meta:
        managed = False
        db_table = 'polare\".\"plano_individual'


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
    plano_individual = models.ForeignKey(
        PlanoIndividual,
        related_name='entregas',
        on_delete=models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = 'polare\".\"entrega'


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
