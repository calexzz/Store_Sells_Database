import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'shop.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema = f.read()
    conn = get_connection()
    conn.executescript(schema)
    conn.close()
