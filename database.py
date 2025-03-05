import psycopg2
from psycopg2 import sql
import re

class ProductBase:
    def __init__(self, dbname, user, password, host, port, table_name='products'):
        self.table_name = table_name
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = self.connect_to_db()
          
    def create_table(self, tables_params):
        """Создание таблицы, если она не существует."""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(tables_params)  # Без f-строки
            table_name = re.search(r'CREATE TABLE IF NOT EXISTS (\w+)', tables_params)
            if table_name:
                self.table_name = table_name.group(1)
            conn.commit()

    def connect_to_db(self):
        """Подключение к базе данных PostgreSQL."""
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port)
            return conn
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise
    
