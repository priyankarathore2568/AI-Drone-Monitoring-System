from django.urls import path
from .views import AnalyticsSummaryView, dashboard_view, DetectionListView


urlpatterns = [
    path("summary/", AnalyticsSummaryView.as_view(), name="analytics-summary"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("detections/", DetectionListView.as_view(), name="detection-list"),
]