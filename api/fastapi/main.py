from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return{"message": "Hello from Fast API"}

@app.get("/hello")
def say_hello():
    return {"message": "Hello Manish"}

# Path parameter -> part of URL -> /student/1 -> http://127.0.0.1:8000/student/101
@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id}

# Query Parameter -> after ? -> /search?q=test -> http://127.0.0.1:8000/search?q=manish
@app.get("/search")
def search(q: str):
    return {"query": q}