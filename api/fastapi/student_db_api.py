from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )


# BaseModel -> request body validation
class Student(BaseModel):
    name: str
    maths: int
    science: int
    english: int


# Get all students
@app.get("/students")
def get_students():
    conn = None
    cursor = None

    try:
        conn = get_connection()
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

        return {
            "success": True,
            "data": students
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# Add student
@app.post("/students")
def add_student(student: Student):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, maths, science, english) VALUES (%s, %s, %s, %s) RETURNING id;",
            (student.name, student.maths, student.science, student.english)
        )

        new_id = cursor.fetchone()[0]
        conn.commit()

        return {
            "success": True,
            "message": "Student added",
            "id": new_id
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# Get student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = %s;", (student_id,))
        row = cursor.fetchone()

        if row:
            return {
                "success": True,
                "data": {
                    "id": row[0],
                    "name": row[1],
                    "maths": row[2],
                    "science": row[3],
                    "english": row[4]
                }
            }

        return {
            "success": False,
            "error": "Student not found"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE students
            SET name = %s, maths = %s, science = %s, english = %s
            WHERE id = %s
            RETURNING id;
            """,
            (student.name, student.maths, student.science, student.english, student_id)
        )

        updated = cursor.fetchone()
        conn.commit()

        if updated:
            return {
                "success": True,
                "message": "Student updated successfully",
                "id": updated[0]
            }

        return {
            "success": False,
            "error": "Student not found"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = %s RETURNING id;",
            (student_id,)
        )

        deleted = cursor.fetchone()
        conn.commit()

        if deleted:
            return {
                "success": True,
                "message": "Student deleted",
                "id": deleted[0]
            }

        return {
            "success": False,
            "error": "Student not found"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()