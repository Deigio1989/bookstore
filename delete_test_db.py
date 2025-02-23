import psycopg2
from psycopg2 import sql
import os

# Defina a URL do banco de dados corretamente
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:qTFCTSU6ZIIydeLWML4ZAhjMQPQUT33c@dpg-cuton8i3esus73ebv2bg-a.oregon-postgres.render.com/bookstore_ebac_sql')

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

try:
    cur.execute(sql.SQL("DROP DATABASE IF EXISTS test_bookstore_ebac_sql"))
except Exception as e:
    print(f"Erro ao excluir o banco de dados: {e}")

cur.close()
conn.close()
