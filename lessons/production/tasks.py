from pathlib import Path
from time import monotonic, sleep

from celery import Celery

app = Celery("reports", broker="redis://localhost:6379/0")
app.conf.task_default_queue = "report-update"
app.conf.worker_prefetch_multiplier = 1
VERSION = "v1"


@app.task(name="tasks.build_report", acks_late=True)
def build_report(request_id: int) -> str:
    if request_id == 81:
        deadline = monotonic() + 300
        while not Path("continue-81").exists():
            if monotonic() >= deadline:
                raise TimeoutError("Истекло время ожидания файла continue-81")
            sleep(0.2)
    path = Path("reports") / f"{request_id}.txt"
    path.parent.mkdir(exist_ok=True)
    path.write_text(f"{VERSION} {request_id}\n", encoding="utf-8")
    return str(path)
