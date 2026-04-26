from db.connection import get_connection

class EmployerRepository:
    def is_cashier(self, id):
        conn = get_connection()
        row = conn.execute(
            '''SELECT e.id FROM employers e
               JOIN job_titles j ON e.id_job_titile = j.id
               WHERE e.id = ? AND j.name IN ('Кассир', 'Старший кассир')''',
            (id,)
        ).fetchone()
        conn.close()
        return row is not None