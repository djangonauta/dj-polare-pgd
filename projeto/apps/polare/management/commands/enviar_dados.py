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
                        filename=options['arquivo_log'],
                        format='[%(asctime)s][%(levelname)s] "[%(message)s]"')


class ClientePGD:

    def __init__(self):
        self.total_registros = 0

    async def main(self):
        logger.info('Processamento inicializado.')
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{settings.PGD_LOGIN_URL}', data=settings.CREDENCIAIS) as response:
                conteudo = await response.json()
                if 'access_token' not in conteudo:
                    raise exceptions.CredencialPGDInvalida('Credenciais (login e/ou senha) inválidas.')

                headers = dict(Authorization=f'Bearer {conteudo["access_token"]}')

            planos = models.PlanoIndividual.objects.prefetch_related('entregas__subtarefas').all()
            async for plano in planos:
                url = f'{settings.PGD_PLANO_TRABALHO_URL}/{plano.id}'
                json = await self.serializar(plano)
                async with session.put(url, json=json, headers=headers) as response:
                    if response.status == 200:
                        logger.info(f'Registro {json["cod_plano"]} cadastrado com sucesso.')
                        self.total_registros += 1
                        continue

                    conteudo = await response.json()
                    if response.status == 422:
                        stream = io.StringIO()
                        pprint.pprint(conteudo, stream=stream)

                        erro = f'Formato inválido dos dados enviados.\n{stream.getvalue()}'
                        raise exceptions.EntidadeNaoProcessada(erro)

                    logger.info(f'Erro ao cadastrar registro {json["cod_plano"]}\n{conteudo}')

        logger.info('Processamento finalizado.')

    @sync_to_async
    def serializar(self, plano):
        return serializers.PlanoIndividualSerializer(instance=plano).data


class Command(BaseCommand):

    def add_arguments(self, parser):
        arquivo_log = f'{datetime.datetime.now().isoformat(timespec="seconds")}.log'

        parser.add_argument('--level', default='info')
        parser.add_argument('--arquivo-log', default=arquivo_log, dest='arquivo_log')

    def handle(self, *args, **options):
        configurar_logging(options)

        try:
            cliente = ClientePGD()
            asyncio.get_event_loop().run_until_complete(cliente.main())

        except KeyboardInterrupt:
            logger.info('\nOperação cancelada pelo usuário.')
            logger.info(f'Total de registros processados: {cliente.total_registros}')

        except Exception as e:
            logger.info(f'Erro de execução no script: {e}')
