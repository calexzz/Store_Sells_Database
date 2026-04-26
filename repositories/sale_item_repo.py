"""
    заполняем таблицу проданными товарами
"""
from db.connection import get_connection

def create_many(id_check, items):
    conn = get_connection()
    for item in items:
        conn.execute(
            '''INSERT INTO sale_items (id_check, id_product, quantity) VALUES (?, ?, ?)''',
            (id_check, item['id_product'], item['quantity'])
        )
    conn.commit()
    conn.close()