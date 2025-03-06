CREATE DATABASE my_postgres;

-- Проверка существования пользователя и назначение пароля
DO $$
BEGIN
    -- Проверяем, существует ли пользователь test_user
    IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'test_user') THEN
        -- Если пользователь существует, назначаем ему пароль
        ALTER USER test_user WITH PASSWORD 'test1234';
    ELSE
        -- Если пользователь не существует, создаем его и назначаем пароль
        CREATE USER test_user WITH PASSWORD 'test1234';
    END IF;
END $$;

-- Предоставление прав на базу данных пользователю
GRANT ALL PRIVILEGES ON DATABASE my_postgres TO test_user;
