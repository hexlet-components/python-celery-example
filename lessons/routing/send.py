import sys

from tasks import build_report, check_report

request_id = int(sys.argv[1])
report = build_report.delay(request_id)
check = check_report.delay(request_id)
print("Файл готов:", check.get(timeout=30))
print("Путь:", report.get(timeout=30))
