import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = None
cursor = None

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students;")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

except Exception as e:
    print("Error:", e)

finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()