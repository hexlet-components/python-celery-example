from pathlib import Path
from time import sleep

from celery import Celery

app = Celery("reports", broker="redis://localhost:6379/0")
app.conf.broker_transport_options = {"visibility_timeout": 15}


@app.task(acks_late=True)
def build_report(request_id: int) -> str:
    path = Path("reports") / f"{request_id}.txt"
    path.parent.mkdir(exist_ok=True)
    if path.exists():
        print(f"Файл {path} уже готов", flush=True)
        return str(path)

    draft = path.with_suffix(".tmp")
    draft.write_text(f"Заявка {request_id}\n", encoding="utf-8")
    draft.replace(path)
    print(f"Файл {path} записан", flush=True)
    sleep(60)
    return str(path)
