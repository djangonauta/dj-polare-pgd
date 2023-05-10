-- Este script cria os schemas necessários para o projeto. Favor atualizar esse script para incluir novos
-- schemas que foram adicionados ao projeto.

-- Para executar o script rode o seguinte comando a partir do diretório do projeto:
-- sudo -u postgres psql < sql/inicial.sql
\echo 'Este script cria os schemas necessários para o projeto.'
\echo 'Favor informar o banco de dados e seu owner (usuário).\n'

\prompt 'DATABASE: ' db
\prompt 'USER: ' user

\c :db
\echo '\nCriando SCHEMA administrativo autorizado para o usuário' :user
create schema administrativo authorization :user;

\echo '\nCriando SCHEMA arquitetura autorizado para o usuário' :user
create schema arquitetura authorization :user;
