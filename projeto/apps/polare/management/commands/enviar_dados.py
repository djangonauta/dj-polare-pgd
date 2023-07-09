import asyncio
import datetime
import io
import logging
import pprint

import aiohttp
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand

from ... import exceptions, models, serializers

logger = logging.getLogger(__name__)


def configurar_logging(options):
    logging.basicConfig(level=options['level'].upper(), datefmt='%d/%m/%Y %H:%M:%S',
                        format='[%(asctime)s][%(levelname)s] "[%(message)s]"',
                        handlers=[logging.StreamHandler(), logging.FileHandler(options['arquivo_log'])])


class ClientePGD:

    def __init__(self):
        self.total_registros = 0

    async def main(self):
        logger.info('Processamento inicializado.')
        async with aiohttp.ClientSession() as session:
            headers = await self.obter_headers(session)

            planos = models.PlanoIndividual.objects.planos_para_api()

            async for plano in planos:
                url = f'{settings.API_PGD_PLANO_TRABALHO_URL}/{plano.id}'
                json = await self.serializar(plano)
                async with session.put(url, json=json, headers=headers) as response:
                    if response.status == 200:
                        self.total_registros += 1
                        continue

                    conteudo = await response.json()
                    if response.status == 422:
                        stream = io.StringIO()
                        pprint.pprint(conteudo, stream=stream)

                        erro = f'Formato inválido dos dados enviados.\n{stream.getvalue()}'
                        raise exceptions.EntidadeNaoProcessada(erro)

        logger.info('Processamento finalizado.')

    async def obter_headers(self, session):
        async with session.post(f'{settings.API_PGD_LOGIN_URL}', data=settings.API_PGD_CREDENCIAIS) as resp:
            conteudo = await resp.json()
            if 'access_token' not in conteudo:
                raise exceptions.CredencialPGDInvalida('Credenciais (login e/ou senha) inválidas.')

            headers = dict(Authorization=f'Bearer {conteudo["access_token"]}')
            return headers

    @sync_to_async
    def serializar(self, plano):
        return serializers.PlanoIndividualSerializer(instance=plano).data

    def mensagem_sucesso(self):
        return f'Total de registros processados: {self.total_registros}'


class Command(BaseCommand):

    def add_arguments(self, parser):
        arquivo_log = f'enviar-dados-{datetime.datetime.now().isoformat(timespec="seconds")}.log'

        parser.add_argument('--level', default='info')
        parser.add_argument('--arquivo-log', default=arquivo_log, dest='arquivo_log')

    def handle(self, *args, **options):
        configurar_logging(options)

        try:
            cliente = ClientePGD()
            asyncio.get_event_loop().run_until_complete(cliente.main())
            logger.info(cliente.mensagem_sucesso())

        except KeyboardInterrupt:
            logger.info('\nOperação cancelada pelo usuário.')
            logger.info(cliente.mensagem_sucesso())

        except Exception as e:
            logger.error(f'Erro de execução no script: {e}', exc_info=True)
