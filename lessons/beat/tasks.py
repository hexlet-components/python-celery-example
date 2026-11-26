from datetime import datetime, timezone
from pathlib import Path

from celery import Celery

app = Celery(
    "reports",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)


@app.task(name="reports.build")
def build_report(request_id: int) -> str:
    path = Path("reports") / f"{request_id}.txt"
    path.parent.mkdir(exist_ok=True)
    path.write_text(datetime.now(timezone.utc).isoformat(), encoding="utf-8")
    return str(path)
