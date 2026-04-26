"""
    создание чека, функция возвращает id чека
"""

from db.connection import get_connection

class ReceiptRepository:
    def create(self, created_at, id_cashier):
        conn = get_connection()
        cursor = conn.execute(
            '''INSERT INTO receipt (created_at, id_cashier) VALUES (?, ?)''',
            (created_at, id_cashier)
        )
        conn.commit()
        id_check = cursor.lastrowid
        conn.close()
        return id_check