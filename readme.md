Instalação
==========

As seguintes váriaveis devem ser definidas no arquivo projeto/settings/.env (exemplos):

    SECRET_KEY='ztibsdwjar1v1pnp-6osx@r(1@!mfklak0$acg9^l^ut!7!sf1'
    DATABASE_URL='postgres://postgres:admin@localhost:5432/polaredb'
    ADMINS='admin=admin@domain.com'
    EMAIL_URL='consolemail://:@'
    API_PGD_LOGIN_URL=http://localhost:5057/auth/jwt/login
    API_PGD_PLANO_TRABALHO_URL=http://localhost:5057/plano_trabalho
    API_PGD_USERNAME=username@domain.com
    API_PGD_PASSWORD=admin


Problemas Identificados
=======================

Os códigos de unidade do IFPA podem ultrapassar o limite de tamanho do tipo integer. Foi alterado o tipo de
dados da coluna cod_unidade_exercicio da tabela public.plano_trabalho de integer para bigint no banco de dados
api_pgd para contornar o erro a seguir:

```bash
sqlalchemy.exc.DataError: (psycopg2.errors.NumericValueOutOfRange) integer out of range
```

O comando SQL utilizado foi o seguinte:

```sql
api_pgd=# alter table public.plano_trabalho alter cod_unidade_exercicio type bigint;
```
