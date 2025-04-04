import logging

import aiohttp
import rich.console
import rich.live
from asgiref.sync import sync_to_async
from django.conf import settings

from . import exceptions, models, serializers

logger = logging.getLogger(__name__)
console = rich.console.Console()


class ClientePGD:
    def __init__(self):
        self.total_participantes = 0

    async def atualizar_participantes(self):
        logger.info('Atualizando participantes.')
        async with aiohttp.ClientSession() as session:
            headers = await self.obter_headers(session)
            planos_qs = await sync_to_async(models.PlanoIndividual.objects.planos_para_api)()
            async for plano in planos_qs:
                url = (f'{settings.API_PGD_URL}/organizacao/SIAPE/'
                       f'{settings.API_PGD_CODIGO_DA_UNIDADE_AUTORIZADORA}/'
                       f'{plano.unidade_localizacao.codigo}/'
                       f'participante/{plano.siape_fill}')

                logger.info(f'Atualizando participante {plano.siape}')
                json = plano.participante

                async with session.put(url, json=json, headers=headers) as response:
                    if response.status == 200:
                        self.total_participantes += 1
                        logger.info(f'Participante ({plano.siape}) '
                                    'atualizado com sucesso.')

                    conteudo = await response.json()
                    if response.status == 422:
                        raise exceptions.EntidadeNaoProcessada(conteudo)

        logger.info(f'{self.total_participantes} participantes atualizados.')

    async def main(self):
        await self.atualizar_participantes()
        logger.info('Processamento finalizado.')

    async def obter_headers(self, session):
        async with session.post(f'{settings.API_PGD_URL}/token', data=settings.API_PGD_CREDENCIAIS) as resp:
            conteudo = await resp.json()
            if 'access_token' not in conteudo:
                raise exceptions.CredencialPGDInvalida('Credenciais (login e/ou senha) inválidas.')

            return dict(Authorization=f'Bearer {conteudo["access_token"]}')

    @sync_to_async
    def serializar(self, plano):
        return serializers.PlanoIndividualSerializer(instance=plano).data

    def mensagem_sucesso(self):
        return f'Total de registros processados: {self.total_participantes}'
