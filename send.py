from tasks import build_report

job = build_report.delay(42)
print(job.id)
