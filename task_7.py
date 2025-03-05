import psycopg2
from psycopg2 import sql
import re
import os


class ProductBase:
    def __init__(self, dbname, user, password, host, port, table_name='products'):
        self.table_name = table_name
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = self.connect_to_db()

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

    def create_table(self, tables_params):
        """Создание таблицы, если она не существует."""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(tables_params)  # Без f-строки
            table_name = re.search(r'CREATE TABLE IF NOT EXISTS (\w+)', tables_params)
            if table_name:
                self.table_name = table_name.group(1)
            conn.commit()

    def show_all_products(self):
        """Вывод всей продукции из таблицы."""
        with self.conn as conn:
            cursor = conn.cursor()
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name))
            cursor.execute(query)
            products = cursor.fetchall()
            print(f"\nВся продукция: ")
            for row in products:
                print(row)

    def add_test_products(self):
        """Добавление тестовых продуктов в таблицу."""
        with self.conn as conn:
            cursor = conn.cursor()
            products = [
                ("Ноутбук", 50000, 15),
                ("Смартфон", 30000, 5),
                ("Планшет", 25000, 8),
                ("Наушники", 5000, 20),
                ("Клавиатура", 2000, 3),
                ("Мышь", 1500, 12),
                ("Монитор", 15000, 7),
                ("Принтер", 10000, 2),
                ("Флешка", 1000, 25),
                ("Кабель", 500, 30)
            ]
            query = sql.SQL("INSERT INTO {} (name, price, quantity) VALUES (%s, %s, %s)").format(sql.Identifier(self.table_name))
            for product in products:
                cursor.execute(query, product)
            conn.commit()

    def get_products_with_low_quantity(self, counts=int(10)):
        """Получение продуктов с количеством меньше переданного значения."""
        with self.conn as conn:
            cursor = conn.cursor()
            query = sql.SQL("SELECT * FROM {} WHERE quantity < %s").format(sql.Identifier(self.table_name))
            cursor.execute(query, (counts,))
            return cursor.fetchall()

    def update_product_price(self, product_name, new_price):
        """Обновление цены продукта по имени."""
        with self.conn as conn:
            cursor = conn.cursor()
            update_query = sql.SQL("UPDATE {} SET price = %s WHERE name = %s").format(sql.Identifier(self.table_name))
            cursor.execute(update_query, (new_price, product_name))

            select_query = sql.SQL("SELECT name, price FROM {} WHERE name = %s").format(sql.Identifier(self.table_name))
            cursor.execute(select_query, (product_name,))
            updated_product = cursor.fetchone()
            conn.commit()
            if updated_product:
                print(f"Новая цена товара '{updated_product[0]}': {updated_product[1]}")
            else:
                print("Товар не найден.")

if __name__ == "__main__":
    table_name = "products6" 
    
    tables_params = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                               id SERIAL PRIMARY KEY,
                               name TEXT NOT NULL,
                               price NUMERIC NOT NULL,
                               quantity INTEGER NOT NULL)'''

    dbname = os.environ["DB_NAME"]
    user = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]


    db = ProductBase(dbname, user, password, host, port)

    # Создание таблицы
    db.create_table(tables_params)

    # Добавление тестовых продуктов
    db.add_test_products()

    db.show_all_products()
    print("--------------")

    # Получение продуктов с количеством меньше 10
    low_quantity_products = db.get_products_with_low_quantity(counts=10)
    print("Продукты с количеством меньше 10:")
    for product in low_quantity_products:
        print(product)
    print("--------------")

    # Обновление цены продукта "Смартфон"
    db.update_product_price("Смартфон", 35000)
    print("Цена продукта 'Смартфон' обновлена.")
