from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

ToDo_db = {}
class Task(BaseModel):
    name : str
    done : bool = False
class TaskEdit(BaseModel):
    id : int
    name : Optional[str]
class TaskDone(BaseModel):
    id : int
    done : bool = True
class Sure(BaseModel):
    sure : bool = False

@app.get("/")
def get_data():
    return ToDo_db

@app.post("/")
def set_task(task:Task):
    task_id = len(ToDo_db)
    ToDo_db[task_id] = {"task_name" : task.name , "task_done" :task.done}
    return {'task_id' : task_id , 'task_name' : task.name , 'task_done' : task.done}
@app.put("/")
def edit_task(task:TaskEdit):
    ans = {task.id : {} }
    if task.name:
        ToDo_db[task.id]["task_name"] = task.name
        ans[task.id]["task_name"] = task.name
    return ans
@app.post("/done")
def task_done(task:TaskDone):
    ans = {task.id : {}}
    if task.done :
        ToDo_db[task.id]["task_done"] = task.done
        ans[task.id]["task_done"] = task.done
    return ans
@app.delete("/clean")
def clean(sure:Sure):
    global ToDo_db
    ans = {}
    if sure.sure:
        for i in ToDo_db:
            if not ToDo_db[i]["task_done"]:
                ans[i] = ToDo_db[i]
                ans[i]["task_done"] = ToDo_db[i]["task_done"]
    ToDo_db = ans
    return ToDo_db