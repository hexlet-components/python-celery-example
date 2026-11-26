import sys

from tasks import app

name = sys.argv[1]
request_id = int(sys.argv[2])
queue = "reports"
job = app.send_task(name, args=(request_id,), queue=queue)
print(job.id, name, queue)
