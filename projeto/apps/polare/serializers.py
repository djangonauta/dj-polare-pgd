from rest_framework import serializers

from . import models


class EntregaSerializer(serializers.ModelSerializer):

    id_atividade = serializers.IntegerField(source='id')
    nome_atividade = serializers.CharField(source='titulo')
    faixa_complexidade = serializers.CharField(source='atividade.complexidade_atividade',
                                               default='NAO_INFORMADA')

    class Meta:
        model = models.Entrega
        fields = ['id_atividade', 'nome_atividade', 'faixa_complexidade', 'tempo_presencial_estimado',
                  'tempo_presencial_programado', 'tempo_teletrabalho_estimado',
                  'tempo_teletrabalho_programado']


class PlanoIndividualSerializer(serializers.ModelSerializer):

    cod_plano = serializers.IntegerField(source='id')
    matricula_siape = serializers.CharField(source='siape')
    cpf = serializers.CharField(default='80644414200')
    nome_participante = serializers.CharField(source='nome')
    cod_unidade_exercicio = serializers.IntegerField(source='unidade_localizacao.codigo')
    nome_unidade_exercicio = serializers.CharField(source='unidade_localizacao.nome')
    modalidade_execucao = serializers.IntegerField(source='modelo_trabalho_numero')
    carga_horaria_semanal = serializers.IntegerField(source='carga_horaria')
    data_inicio = serializers.CharField(default='2022-12-12')
    data_fim = serializers.CharField(default='2023-05-12')
    carga_horaria_total = serializers.IntegerField()
    horas_homologadas = serializers.IntegerField(source='carga_horaria')

    atividades = EntregaSerializer(source='entregas', many=True)

    class Meta:
        model = models.PlanoIndividual
        fields = ['cod_plano', 'matricula_siape', 'cpf', 'nome_participante',
                  'cod_unidade_exercicio', 'nome_unidade_exercicio', 'modalidade_execucao',
                  'carga_horaria_semanal', 'data_inicio', 'data_fim', 'carga_horaria_total',
                  'horas_homologadas', 'atividades']

    def to_representation(self, instance):
        if instance.carga_horaria > 40:
            instance.carga_horaria = 40

        return super().to_representation(instance)
