from types import MethodType

from django.db import connections
from django.test.runner import DiscoverRunner


def prepare_database(self):
    schemas = ['administrativo', 'arquitetura']
    comandos = map(lambda s: f'create schema {s}', schemas)
    self.connect()
    self.connection.cursor().execute(';'.join(comandos))


class PostgresSchemaTestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        for connection_name in connections:
            connection = connections[connection_name]
            connection.prepare_database = MethodType(prepare_database, connection)

        return super().setup_databases(**kwargs)
