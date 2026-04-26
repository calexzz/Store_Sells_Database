"""
    запрос всех продуктов по категориям и количеством на складе
"""

from db.connection import get_connection

def get_all():
    conn = get_connection()
    rows = conn.execute(
        '''SELECT p.id_product, p.name_of_product, p.price, 
                  p.quantity_at_storage, c.name_of_category
           FROM products p
           JOIN categories c ON p.id_category = c.id_category'''
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
