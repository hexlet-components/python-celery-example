from celery import shared_task
from django.conf import settings

from .models import ReportRequest


@shared_task
def build_report(request_id: int) -> str:
    report = ReportRequest.objects.get(pk=request_id)
    path = settings.BASE_DIR / "output" / "reports" / f"{report.pk}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"Отчёт по заявке {report.pk}\n", encoding="utf-8")
    return str(path)
