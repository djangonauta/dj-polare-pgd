from rest_framework import serializers

from . import models


class EntregaSerializer(serializers.ModelSerializer):

    id_atividade = serializers.IntegerField(source='id')
    nome_atividade = serializers.CharField(source='titulo')
    qtde_entregas = serializers.IntegerField(source='subtarefas.count')

    class Meta:
        model = models.Entrega
        fields = ['id_atividade', 'nome_atividade', 'qtde_entregas']


class PlanoIndividualSerializer(serializers.ModelSerializer):

    cod_plano = serializers.IntegerField(source='id')
    matricula_siape = serializers.CharField(source='siape')
    nome_participante = serializers.CharField(source='nome')
    cod_unidade_exercicio = serializers.CharField(source='unidade_localizacao.codigo')
    nome_unidade_exercicio = serializers.CharField(source='unidade_localizacao.nome')
    modalidade_execucao = serializers.CharField(source='modelo_trabalho')
    carga_horaria_semanal = serializers.IntegerField(source='carga_horaria')
    carga_horaria_total = serializers.IntegerField(source='carga_horaria')
    atividades = EntregaSerializer(source='entregas', many=True)

    class Meta:
        model = models.PlanoIndividual
        fields = ['cod_plano', 'situacao', 'matricula_siape', 'nome_participante', 'cod_unidade_exercicio',
                  'nome_unidade_exercicio', 'modalidade_execucao', 'carga_horaria_semanal',
                  'carga_horaria_total',
                  'atividades']
