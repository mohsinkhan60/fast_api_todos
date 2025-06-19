from fastapi import FastAPI

api = FastAPI()

all_todos = [
   {"id": 1, "todo_name": "sports", "todo_description": "play football"},
   {"id": 2, "todo_name": "study", "todo_description": "study fastapi"},
   {"id": 3, "todo_name": "work", "todo_description": "work on project"},
   {"id": 4, "todo_name": "exercise", "todo_description": "go to the gym"},
   {"id": 5, "todo_name": "read", "todo_description": "read a book"}
]

@api.get("/")
def index():
    return {"message": "Hello, World!"}

@api.get("/todos/{id}")
def get_todo(id: int):
    for todo in all_todos:
        if todo["id"] == id:
            return todo
    return {"error": "Todo not found"}

@api.get("/todos")
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
    
@api.post("/todos")
def create_todo(todo: dict):
    new_todo_id = max(todo["id"] for todo in all_todos) + 1
    new_todo = {
        "id": new_todo_id,
        "todo_name": todo["todo_name"],
        "todo_description": todo["todo_description"]
    }
    all_todos.append(new_todo)
    return new_todo

@api.put("/todos/{id}")
def update_todo(id: int, updated_todo: dict):
    for todo in all_todos:
        if todo["id"] == id:
            todo["todo_name"] = updated_todo["todo_name"]
            todo["todo_description"] = updated_todo["todo_description"]
            return todo
    return {"error": "Todo not found"}
        
@api.delete("/todos/{id}")
def delete_todo(id: int):
    for index, todo in enumerate(all_todos):
        if todo["id"] == id:
            del all_todos[index]
            return {"message": "Todo deleted successfully"}
    return {"error": "Todo not found"}