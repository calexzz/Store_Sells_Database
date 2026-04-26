"""
    запрос всех продуктов по категориям, количество на складе, списание позиций
"""

from db.connection import get_connection

class ProductRepository:
    def get_all(self):
        conn = get_connection()
        rows = conn.execute(
            '''SELECT p.id_product, p.name_of_product, p.price, 
                      p.quantity_at_storage, c.name_of_category
               FROM products p
               JOIN categories c ON p.id_category = c.id_category'''
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_quantity(self, id_product):
        conn = get_connection()
        row = conn.execute(
            'SELECT quantity_at_storage FROM products WHERE id_product = ?',
            (id_product,)
        ).fetchone()
        conn.close()
        return row['quantity_at_storage'] if row else 0

    def decrease_quantity(self, id_product, quantity):
        conn = get_connection()
        conn.execute(
            'UPDATE products SET quantity_at_storage = quantity_at_storage - ? WHERE id_product = ?',
            (quantity, id_product)
        )
        conn.commit()
        conn.close()
