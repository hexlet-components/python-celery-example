from pathlib import Path

from celery import Celery, Task

app = Celery(
    "reports",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)


def read_source(request_id: int, retries: int) -> str:
    if request_id <= 0:
        raise ValueError("Номер заявки должен быть положительным")
    if request_id == 42 or retries == 0:
        raise ConnectionError("Источник временно недоступен")
    return f"Заявка {request_id}\n"


@app.task(
    bind=True,
    autoretry_for=(ConnectionError,),
    retry_backoff=2,
    retry_jitter=False,
    max_retries=2,
)
def build_report(self: Task, request_id: int) -> str:
    contents = read_source(request_id, self.request.retries)
    path = Path("reports") / f"{request_id}.txt"
    path.parent.mkdir(exist_ok=True)
    path.write_text(contents, encoding="utf-8")
    return str(path)
