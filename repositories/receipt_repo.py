"""
    создание чека, функция возвращает id чека
"""

from db.connection import get_connection

def create(created_at, id_cashier):
    conn = get_connection()
    cursor = conn.execute(
        '''INSERT INTO receipt (created_at, id_cashier) VALUES (? ?)''',
        (created_at, id_cashier)
    )
    conn.commit()
    id_check = cursor.lastrowid
    conn.close()
    return id_check