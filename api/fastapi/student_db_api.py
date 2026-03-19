from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/students")
def get_students():
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

        students = []
        for row in rows:
            students.append({
                "id": row[0],
                "name": row[1],
                "maths": row[2],
                "science": row[3],
                "english": row[4]
            })

        return students

    except Exception as e:
        return {"error": str(e)}

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()