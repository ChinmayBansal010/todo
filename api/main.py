from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Chinmay's To-Do API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Todo(BaseModel):
    id: int
    task: str
    completed: bool = False

db: List[Todo] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to Chinmay Bansal's To-Do API."}

@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    db.append(todo)
    return todo

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return db

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_task: Todo):
    for index, todo in enumerate(db):
        if todo.id == todo_id:
            db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(db):
        if todo.id == todo_id:
            del db[index]
            return {"message": f"Task {todo_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")