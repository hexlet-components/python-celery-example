from pathlib import Path
from time import sleep

from celery import Celery

app = Celery(
    "reports",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)


@app.task(name="reports.build")
def build_report(request_id: int) -> str:
    sleep(5)
    path = Path("reports") / f"{request_id}.txt"
    path.parent.mkdir(exist_ok=True)
    path.write_text(f"Заявка {request_id}\n", encoding="utf-8")
    return str(path)


@app.task(name="reports.check")
def check_report(request_id: int) -> bool:
    return (Path("reports") / f"{request_id}.txt").is_file()
