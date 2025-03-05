from config import dbname, user, password, host, port
from models import BaseOps

if __name__ == "__main__":
    table_name = "products6"     
    tables_params = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                               id SERIAL PRIMARY KEY,
                               name TEXT NOT NULL,
                               price NUMERIC NOT NULL,
                               quantity INTEGER NOT NULL)'''

    # Инициализация объекта для работы с базой данных
    db = BaseOps(dbname, user, password, host, port, table_name)

    # Создание таблицы
    db.create_table(tables_params)

    # Добавление тестовых продуктов
    db.add_test_products()

    # Вывод всех продуктов
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
