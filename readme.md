Instalação
==========

As seguintes váriaveis devem ser definidas no arquivo projeto/settings/.env (exemplos):

    SECRET_KEY='ztibsdwjar1v1pnp-6osx@r(1@!mfklak0$acg9^l^ut!7!sf1'
    DATABASE_URL='postgres://postgres:admin@localhost:5432/polaredb?options=-c search_path=polare'
    ADMINS='admin=admin@domain.com'
    EMAIL_URL='consolemail://:@'
    BROKER_URL='amqp://igor:123@localhost:5672/projeto'
    PGD_LOGIN_URL=http://localhost:5057/auth/jwt/login
    PGD_PLANO_TRABALHO_URL=http://localhost:5057/plano_trabalho
    USERNAME=username@domain.com
    PASSWORD=admin
