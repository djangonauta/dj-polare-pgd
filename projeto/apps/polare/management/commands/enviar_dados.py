import asyncio
import logging

import rich
from django.core.management.base import BaseCommand

from ... import utils

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            cliente = utils.ClientePGD()
            asyncio.run(cliente.main())
            logger.info(cliente.mensagem_sucesso())

        except KeyboardInterrupt:
            logger.info('\nOperação cancelada pelo usuário.')
            logger.info(cliente.mensagem_sucesso())

        except Exception as e:
            logger.info('Erro de execução no script:')
            rich.print(e)
