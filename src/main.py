import logging
from fastapi import FastAPI, Form, Request, Body
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from celery.result import AsyncResult

from worker import create_task, app as celery_app

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@app.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})

@app.get("/tasks/{task_id}")
def get_status(task_id):
    # see this answer: https://stackoverflow.com/a/30760142/1756032
    # about AsyncResult() class https://docs.celeryproject.org/en/stable/reference/celery.result.html
    task_result = celery_app.AsyncResult(task_id, task_name="create_task")
    # task_result = task_result.get() # this will wait until complete
    # logging.info(task_result.__dict__)
    result = {
        "task_id": task_result.task_id,
        "task_status": task_result.status,
        "state": task_result.state,
        "ready": task_result.ready(),
        "task_result": task_result.result,
    }
    return JSONResponse(result)
