import os
import time
import redis

from celery import Celery


app = Celery(__name__)
app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
app.conf.task_track_started = True # required to ensure task tracking


@app.task(name="create_task", bind=True)
def create_task(self, task_type):
    time.sleep(int(task_type) * 10)
    return True

def celery_worker_ping() -> bool:
    """ Simple PING - PONG Celery Service """
    result = app.control.broadcast('ping', reply=True, limit=1)
    return bool(result)

def redis_ping(host="127.0.0.1", port=6379):
    conn = redis.Redis(host=host, port=port)
    status, message = None, ""
    try:
        status, message = conn.ping(), 'OK'
    except redis.exceptions.RedisError as e:
        status, message = False, str(e)
    return status, message

def celery_worker_details() -> dict:
    """ Check Celery Status - Details """
    insp = app.control.inspect()
    availability = insp.ping()
    stats = insp.stats()
    registered_tasks = insp.registered()
    active_tasks = insp.active()
    scheduled_tasks = insp.scheduled()
    return {
        'availability': availability,
        'stats': stats,
        'registered_tasks': registered_tasks,
        'active_tasks': active_tasks,
        'scheduled_tasks': scheduled_tasks,
    }
"""
worker_process_init
worker_process_shutdown
"""
