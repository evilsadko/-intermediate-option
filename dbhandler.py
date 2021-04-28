from clickhouse_driver import Client
client = Client('localhost')

print (client.execute('SHOW TABLES'))


"""
Мне нужно запихнуть все данные в одну строку для создания колоночной бд
CREATE DATABASE yourdbname;
CREATE USER youruser WITH ENCRYPTED PASSWORD 'yourpass';
CREATE USER newuser WITH LOGIN ENCRYPTED PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE yourdbname TO youruser;
DROP DATABASE [IF EXISTS] database_name;
https://www.postgresqltutorial.com/postgresql-list-users/
DROP USER [USERNAME];
\du
\l+
https://tableplus.com/blog/2018/04/postgresql-how-to-grant-access-to-users.html
https://stackoverflow.com/questions/22483555/postgresql-give-all-permissions-to-a-user-on-a-postgresql-database
https://gist.github.com/pierrejoubert73/85b3ce8b52e7f6dbce69e2636f68383f
https://chartio.com/resources/tutorials/how-to-change-a-user-to-superuser-in-postgresql/
https://stackoverflow.com/questions/2732474/restore-a-postgres-backup-file-using-the-command-line

git add .
git commit -m 'update'
git push --set-upstream origin v0.2

CREATE ROLE name;
ALTER USER name CREATEDB REPLICATION CREATEROLE BYPASSRLS LOGIN;
ALTER USER name CREATEDB;
ALTER USER name REPLICATION;
ALTER USER name CREATEROLE;
ALTER USER name BYPASSRLS;
ALTER USER name LOGIN;
ALTER USER name WITH SUPERUSER;

pg_restore -d b24online b24online.com-2021-04-26.psql - перед этим создаю бд и роль с именем совпадающим в бд
pg_restore b24online.com-2021-04-26.psql - старая версия, создаю роль в бд с именем супер пользователя, назначаю привелегии, из консоли автоматически создается

\c name_db
\dt смотрю все таблици

"""
