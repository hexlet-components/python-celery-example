from tasks import build_report

jobs = [build_report.delay(41), build_report.delay(42)]
for job in jobs:
    print(job.id)

for job in jobs:
    outcome = job.get(timeout=30, propagate=False)
    print(job.id, job.state, str(outcome))
