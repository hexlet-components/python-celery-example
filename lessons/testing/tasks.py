from pathlib import Path

from celery import Celery

app = Celery(
    "reports",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)
app.conf.task_default_queue = "report-tests"


def render_report(request_id: int) -> str:
    return f"Заявка №{request_id}\n"


@app.task
def build_report(request_id: int) -> str:
    path = Path("reports") / f"{request_id}.txt"
    path.parent.mkdir(exist_ok=True)
    path.write_text(render_report(request_id), encoding="utf-8")
    return str(path)
