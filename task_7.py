import psycopg2
from psycopg2 import sql
from database import ProductBase
from config import dbname, user, password, host, port
import re


class BaseOps(ProductBase):
    def __init__(self, dbname, user, password, host, port, table_name='products'):
        super().__init__(dbname, user, password, host, port, table_name)
    
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

