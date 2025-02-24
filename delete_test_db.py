import psycopg2
from psycopg2 import sql
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://yourusername:yourpassword@localhost:5432/bookstore')
print(f"Connecting to database with URL: {DATABASE_URL}")

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(sql.SQL("DROP DATABASE IF EXISTS test_bookstore_ebac_sql"))
        print("Test database 'test_bookstore_ebac_sql' dropped successfully.")
    except Exception as e:
        print(f"Erro ao excluir o banco de dados: {e}")

    cur.close()
    conn.close()
except Exception as conn_err:
    print(f"Erro ao conectar ao banco de dados: {conn_err}")
