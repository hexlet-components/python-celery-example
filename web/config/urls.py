from django.urls import path
from django.views.generic import TemplateView
from reports.views import create_report

urlpatterns = [
    path("", TemplateView.as_view(template_name="reports/index.html")),
    path("reports/", create_report),
]
