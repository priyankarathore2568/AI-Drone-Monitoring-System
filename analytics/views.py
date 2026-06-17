from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from drones.models import Drone
from telemetry.models import Telemetry
from deliveries.models import Delivery
from alerts.models import Alert

from rest_framework import generics
from .models import Detection
from .serializers import DetectionSerializer


class AnalyticsSummaryView(APIView):

    def get(self, request):
        data = {
            "total_drones": Drone.objects.count(),
            "active_drones": Drone.objects.filter(status="ACTIVE").count(),
            "maintenance_drones": Drone.objects.filter(status="MAINTENANCE").count(),

            "total_deliveries": Delivery.objects.count(),
            "pending_deliveries": Delivery.objects.filter(status="PENDING").count(),
            "assigned_deliveries": Delivery.objects.filter(status="ASSIGNED").count(),
            "delivered_deliveries": Delivery.objects.filter(status="DELIVERED").count(),

            "total_telemetry_records": Telemetry.objects.count(),

            "total_alerts": Alert.objects.count(),
            "low_battery_alerts": Alert.objects.filter(alert_type="LOW_BATTERY").count(),
            "weak_signal_alerts": Alert.objects.filter(alert_type="WEAK_SIGNAL").count(),
            "high_temperature_alerts": Alert.objects.filter(alert_type="HIGH_TEMPERATURE").count(),
            "unresolved_alerts": Alert.objects.filter(is_resolved=False).count(),
            "obstacle_alerts": Alert.objects.filter(alert_type="OBSTACLE_DETECTED").count(),
            "intruder_alerts": Alert.objects.filter(alert_type="INTRUDER_DETECTED").count(),
            "collision_alerts": Alert.objects.filter(alert_type="COLLISION_WARNING").count(),
        }

        return Response(data)
    
def dashboard_view(request):
    context = {
        "total_drones": Drone.objects.count(),
        "active_drones": Drone.objects.filter(status="ACTIVE").count(),
        "total_deliveries": Delivery.objects.count(),
        "total_telemetry_records": Telemetry.objects.count(),
        "total_alerts": Alert.objects.count(),
        "unresolved_alerts": Alert.objects.filter(is_resolved=False).count(),
        "latest_alerts": Alert.objects.order_by("-created_at")[:5],
        "maintenance_drones": Drone.objects.filter(status="MAINTENANCE").count(),
        
        "inactive_drones": Drone.objects.filter(status="INACTIVE").count(),
        "low_battery_alerts": Alert.objects.filter(alert_type="LOW_BATTERY").count(),
        "weak_signal_alerts": Alert.objects.filter(alert_type="WEAK_SIGNAL").count(),
        "high_temperature_alerts": Alert.objects.filter(alert_type="HIGH_TEMPERATURE").count(),
        
        "obstacle_alerts": Alert.objects.filter(alert_type="OBSTACLE_DETECTED").count(),
        "intruder_alerts": Alert.objects.filter(alert_type="INTRUDER_DETECTED").count(),
        "collision_alerts": Alert.objects.filter(alert_type="COLLISION_WARNING").count(),
        
        "pending_deliveries": Delivery.objects.filter(status="PENDING").count(),
        "assigned_deliveries": Delivery.objects.filter(status="ASSIGNED").count(),
        "delivered_deliveries": Delivery.objects.filter(status="DELIVERED").count(),
        "failed_deliveries": Delivery.objects.filter(status="FAILED").count(),
        
        "total_detections": Detection.objects.count(),
        "person_detections": Detection.objects.filter(object_type="PERSON").count(),
        "car_detections": Detection.objects.filter(object_type="CAR").count(),
        "bus_detections": Detection.objects.filter(object_type="BUS").count(),
        "truck_detections": Detection.objects.filter(object_type="TRUCK").count(),
        "motorcycle_detections": Detection.objects.filter(object_type="MOTORCYCLE").count(),
        "critical_detections": Detection.objects.filter(risk_level="CRITICAL").count(),
        "latest_detections": Detection.objects.all().order_by("-detected_at")[:5],
    }

    return render(request, "dashboard.html", context)


class DetectionListView(generics.ListAPIView):
    queryset = Detection.objects.all().order_by("-detected_at")
    serializer_class = DetectionSerializer