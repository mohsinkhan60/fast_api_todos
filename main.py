from enum import IntEnum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

api = FastAPI()

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=500, description="Name of the todo")
    todo_description: str = Field(..., description="Description of the todo")
    priority: Priority = Field(default = Priority.LOW, description="Priority of the todo")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int = Field(..., description="Unique identifier for the todo") 

class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=500, description="Name of the todo")
    todo_description: Optional[str] = Field(None, description="Description of the todo")
    priority: Optional[Priority] = Field(default = Priority.LOW, description="Priority of the todo")



all_todos = [
    Todo(id=1, todo_name="sports", todo_description="play football", priority=Priority.HIGH),
    Todo(id=2, todo_name="study", todo_description="study fastapi", priority=Priority.MEDIUM),
    Todo(id=3, todo_name="shopping", todo_description="buy groceries", priority=Priority.LOW),
    Todo(id=4, todo_name="exercise", todo_description="go to the gym", priority=Priority.LOW),
    Todo(id=5, todo_name="reading", todo_description="read a book", priority=Priority.MEDIUM),
]

@api.get("/todos/{id}", response_model=Todo)
def get_todo(id: int):
    for todo in all_todos:
        if todo.id == id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@api.get("/todos", response_model=List[Todo])
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
    
@api.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.id for todo in all_todos) + 1
    new_todo = Todo(
        id=new_todo_id,
        todo_name=todo.todo_name,
        todo_description=todo.todo_description,
        priority=todo.priority
    )
    all_todos.append(new_todo)
    return new_todo

@api.put("/todos/{id}", response_model=Todo)
def update_todo(id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.id == id:
            if updated_todo.todo_name is not None:
                todo.todo_name = updated_todo.todo_name
            if updated_todo.todo_description is not None:
                todo.todo_description = updated_todo.todo_description
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
        
@api.delete("/todos/{id}", response_model=Todo)
def delete_todo(id: int):
    for index, todo in enumerate(all_todos):
        if todo.id == id:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    raise HTTPException(status_code=404, detail="Todo not found")