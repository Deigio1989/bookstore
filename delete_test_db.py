import psycopg2
from psycopg2 import sql
import os

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

try:
    cur.execute(sql.SQL("DROP DATABASE IF EXISTS test_bookstore_ebac_sql"))
except Exception as e:
    print(f"Erro ao excluir o banco de dados: {e}")

cur.close()
conn.close()
