"""
    заполнение таблиц данными из csv-файлов
"""

import csv
import os
from db.connection import get_connection

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def seed():
    conn = get_connection()

    for row in load_csv('job_titles.csv'):
        conn.execute(
            'INSERT OR IGNORE INTO job_titles (id, name) VALUES (?, ?)',
            (row['id'], row['name'])
        )

    for row in load_csv('categories.csv'):
        conn.execute(
            'INSERT OR IGNORE INTO categories (id_category, name_of_category) VALUES (?, ?)',
            (row['id_category'], row['name_of_category'])
        )

    for row in load_csv('employers.csv'):
        conn.execute(
            'INSERT OR IGNORE INTO employers (id, name, surname, id_job_titile) VALUES (?, ?, ?, ?)',
            (row['id'], row['name'], row['surname'], row['id_job_title'])
        )

    for row in load_csv('products.csv'):
        conn.execute(
            'INSERT OR IGNORE INTO products (id_product, name_of_product, price, id_category, quantity_at_storage) VALUES (?, ?, ?, ?, ?)',
            (row['id_product'], row['name_of_product'], row['price'], row['id_category'], row['quantity_at_storage'])
        )

    conn.commit()
    conn.close()
    print("Данные загружены")

if __name__ == '__main__':
    seed()