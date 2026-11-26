import sys
from pathlib import Path

from celery.exceptions import TimeoutError

from tasks import app

job = app.AsyncResult(sys.argv[1])
print(job.state)
try:
    filename = job.get(timeout=3)
except TimeoutError:
    print("За три секунды результат не получен")
else:
    print(Path(filename).read_text(encoding="utf-8").strip())
