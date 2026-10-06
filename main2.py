from fastapi import FastAPI,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional,List
from models import TodoModel
from database import SessionLocal,engine

app=FastAPI()
TodoModel.metadata.create_all(bind=engine)  # create the table in the database

# todos=[] # create an empty list to store todos, in memory db

class TodoBase(BaseModel):
    title:str
    description:Optional[str]=None
    completed:bool=False

class TodoCreate(BaseModel):
    pass

class TodoUpdate(BaseModel):
    pass

class TodoResponse(BaseModel):
    id:int
    title: str
    description: Optional[str] = None
    completed: bool = False
    class Config:               # this part is telling Pydantic how to convert a SQLAlchemy object into a Pydantic response. means it allows "Pydantic to read data from ORM/SQLAlchemy objects using their attributes."
        from_attributes=True          

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/todos",response_model=List[TodoResponse])
def get_todos(db:Session=Depends(get_db)):
    todos=db.query(TodoModel).all()
    return todos

@app.get("/todos/{todos_id}",response_model=TodoResponse)
def get_todo(todos_id:int,db:Session=Depends(get_db)):
    todos=db.query(TodoModel).filter(TodoModel.id==todos_id).first()
    return todos

@app.post("/todos",response_model=TodoResponse)
def create_todo(todo:TodoBase,db:Session=Depends(get_db)):
    db_todo=TodoModel(title=todo.title,description=todo.description,completed=todo.completed)  
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todos_id}",response_model=TodoResponse)
def delete_todo(todos_id:int,db:Session=Depends(get_db)):
    todos=db.query(TodoModel).filter(TodoModel.id==todos_id).first()
    db.delete(todos)
    db.commit()
    return todos

@app.put("/todos/{todos_id}",response_model=TodoResponse)
def update_todo(todos_id:int,updated_todo:TodoBase,db:Session=Depends(get_db)):
    find_id=db.query(TodoModel).filter(TodoModel.id==todos_id).first()
    if find_id is None:
        return {'error':'Todo not found'}
    find_id.title=updated_todo.title
    find_id.description=updated_todo.description
    find_id.completed=updated_todo.completed
    db.commit()
    db.refresh(find_id)
    return find_id
    
    