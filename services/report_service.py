import datetime
from db.connection import get_connection

class ReportService:
    def day_range(self, date: datetime.date):
        """Возвращает unix timestamp начала и конца дня"""
        start = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        end   = datetime.datetime(date.year, date.month, date.day, 23, 59, 59)
        return start.timestamp(), end.timestamp()

    def daily_report(self, date: datetime.date):
        """
        Возвращает словарь:
        {
            'items': [{'name_of_product': ..., 'quantity': ..., 'total': ...}, ...],
            'revenue': 123.45
        }
        """
        start, end = self.day_range(date)
        conn = get_connection()

        rows = conn.execute(
            '''SELECT p.name_of_product,
                      SUM(si.quantity) AS quantity,
                      SUM(si.quantity * p.price) AS total
               FROM sale_items si
               JOIN receipt r ON si.id_check = r.id_check
               JOIN products p ON si.id_product = p.id_product
               WHERE r.created_at BETWEEN ? AND ?
               GROUP BY p.id_product''',
            (start, end)
        ).fetchall()

        conn.close()

        items = [dict(row) for row in rows]
        revenue = sum(item['total'] for item in items)

        return {'items': items, 'revenue': revenue}