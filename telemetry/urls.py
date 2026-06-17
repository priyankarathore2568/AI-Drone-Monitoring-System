from django.urls import path
from .views import TelemetryListView, TelemetryDetailView


urlpatterns = [
    path("telemetry/", TelemetryListView.as_view(), name="telemetry-list"),
    path("telemetry/<int:id>/", TelemetryDetailView.as_view(), name="telemetry-detail"),
]