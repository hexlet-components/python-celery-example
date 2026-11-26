from django.db import models


class ReportRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
