CREATE DATABASE my_postgres;

-- Создание пользователя и предоставление прав
CREATE USER test_user WITH PASSWORD 'test1234';
GRANT ALL PRIVILEGES ON DATABASE my_postgres TO test_user;


