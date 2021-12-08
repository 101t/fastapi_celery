# Asynchronouns Tasks using FastAPI + Celery

## Run service

```sh
docker-compose up -d --build
```
Open your browser on [http://localhost:8000](http://localhost:8000) to check the app also you may check Celery Flower through [http://localhost:8080](http://localhost:8080)

## Testing service

Trigger a new task:
```sh
curl http://localhost:8000/tasks -H "Content-Type: application/json" --data '{"type": 0}'
```

To Get Status:
```sh
curl http://localhost:8000/tasks/<task_id>
```