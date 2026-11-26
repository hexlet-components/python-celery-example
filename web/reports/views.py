from functools import partial

from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from .models import ReportRequest
from .tasks import build_report


@require_POST
def create_report(request: HttpRequest) -> JsonResponse:
    with transaction.atomic():
        report = ReportRequest.objects.create()
        transaction.on_commit(partial(build_report.delay, report.pk))
    return JsonResponse({"request_id": report.pk}, status=202)
