Instalação
==========

As seguintes váriaveis devem ser definidas no arquivo projeto/settings/.env (exemplos):

    SECRET_KEY='ztibsdwjar1v1pnp-6osx@r(1@!mfklak0$acg9^l^ut!7!sf1'
    DATABASE_URL='postgres://postgres:admin@localhost:5432/polaredb'
    ADMINS='admin=admin@domain.com'
    EMAIL_URL='consolemail://:@'
    PGD_LOGIN_URL=http://localhost:5057/auth/jwt/login
    PGD_PLANO_TRABALHO_URL=http://localhost:5057/plano_trabalho
    USERNAME=username@domain.com
    PASSWORD=admin


Problemas Identificados
=======================

Os códigos de unidade do IFPA podem ultrapassar o limite de tamanho do tipo integer. Foi alterado o tipo de
dados da coluna cod_unidade_exercicio da tabela public.plano_trabalho de integer para bigint no banco de dados
api_pgd.
