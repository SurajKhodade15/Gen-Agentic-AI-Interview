
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel, Field

app = FastAPI()


class Student(BaseModel):
    name: str = Field(..., example="John Doe")
    age: int = Field(..., example=20)
    courses: List[str] = Field(..., example=["Math", "Science", "History"])

@app.get("/")
async def index():
    return {"message": "Hello, World!"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/hello")
async def hello(name:str, age:int):
    return {"name": name, "age": age}


@app.post("/students")
async def student_info(student: Student):
    return {"message": "Student information received", "student": student}