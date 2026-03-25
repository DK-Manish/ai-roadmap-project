from fastapi import FastAPI
# Pydantic -> Python library used for data validation and parsing using type hints
# BaseModel - > Class in Pydantic used to define the structure of data and automatically validate incoming data against it
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return{"message": "Hello from Fast API"}

@app.get("/hello")
def say_hello():
    return {"message": "Hello Manish"}

# Path parameter -> part of URL -> /student/1 -> http://127.0.0.1:8000/student/101
# @app.get("/students/{student_id}")
# def get_student(student_id: int):
#     return {"student_id": student_id}

# Query Parameter -> after ? -> /search?q=test -> http://127.0.0.1:8000/search?q=manish
@app.get("/search")
def search(q: str):
    return {"query": q}

class Student(BaseModel):
    id: int
    name: str
    marks: int

# Store the student deatils
students = []

# Create student records
@app.post("/student")
def create_student(student: Student):
    students.append(student)
    return student

# List all students records
@app.get("/students")
def get_all_students():
    return students

# List students records based on ID
@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    for student in students:
        if student.id == student_id:
            return student
    return {"error": "Student not found"}

# Put records
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for i, student in enumerate(students):
        if student.id == student_id:
            students[i] = updated_student
            return updated_student
    return {"error": "Student not found"}

# Delete a student record
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i, student in enumerate(students):
        if student.id == student_id:
            deleted_student = students.pop(i)
            return {
                "message": "Student deleted successfully",
                "student": deleted_student
            }
    return {"error": "Student not found"}