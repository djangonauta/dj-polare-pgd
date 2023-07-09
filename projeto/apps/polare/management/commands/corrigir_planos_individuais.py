from django.core.management.base import BaseCommand
from ... import models
import logging
import datetime


logger = logging.getLogger(__name__)


def configurar_logging(options):
    logging.basicConfig(level=options['level'].upper(), datefmt='%d/%m/%Y %H:%M:%S',
                        format='[%(asctime)s][%(levelname)s] "[%(message)s]"',
                        handlers=[logging.StreamHandler(), logging.FileHandler(options['arquivo_log'])])


class Command(BaseCommand):

    def add_arguments(self, parser):
        tempo = datetime.datetime.now().isoformat(timespec="seconds")
        arquivo_log = f'corrigir-planos-individuais-{tempo}.log'
        parser.add_argument('--arquivo-log', default=arquivo_log, dest='arquivo_log')
        parser.add_argument('--level', default='info')

        parser.add_argument('ano_referencia', type=int)

    def handle(self, *args, **options):
        configurar_logging(options)
        for plano in models.PlanoIndividual.objects.filter(ano_referencia=options['ano_referencia'],
                                                           ativo=True):
            try:
                unidade_plano_individual = plano.unidade_localizacao_id
                plano_gerencial_unidade = models.PlanoGerencialUnidade.objects.get(
                    ano_referencia=options['ano_referencia'],
                    ativo=True,
                    status='HOMOLOGADO',
                    id_unidade_localizacao=unidade_plano_individual
                )
                if plano.plano_gerencial_unidade.id != plano_gerencial_unidade.id:
                    logger.info(f'Atualizando plano individual {plano.id}: alterando plano gerencial de '
                                f'{plano.plano_gerencial_unidade.id} para {plano_gerencial_unidade.id}')

                    plano.plano_gerencial_unidade = plano_gerencial_unidade
                    plano.save()

            except models.PlanoGerencialUnidade.DoesNotExist:
                logger.info(
                    f'Não foi encontrado plano gerencial para a unidade {unidade_plano_individual}')

            except models.PlanoGerencialUnidade.MultipleObjectsReturned:
                logger.info(
                    f'Foram encontrados mais de 1 plano gerencial para a unidade {unidade_plano_individual}'
                )
