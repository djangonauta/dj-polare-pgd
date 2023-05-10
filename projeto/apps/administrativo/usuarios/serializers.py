from django.contrib import auth
from rest_framework import serializers


class UsuarioSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        # return dict(id=instance.id, text=instance.nome_completo) # select2
        return super().to_representation(instance)

    class Meta:
        model = auth.get_user_model()
        fields = ['id', 'username', 'perfil_imagem', 'nome_completo']


class DisableSignupSerializer(serializers.Serializer):

    def validate(self, data):
        raise serializers.ValidationError('Registro de novas contas temporariamente suspenso.')
