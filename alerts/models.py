from django.db import models

# Create your models here.
from drones.models import Drone
from deliveries.models import Delivery


class Alert(models.Model):
    ALERT_TYPES = [
        ("LOW_BATTERY", "Low Battery"),
        ("WEAK_SIGNAL", "Weak Signal"),
        ("HIGH_TEMPERATURE", "High Temperature"),
        ("OBSTACLE_DETECTED", "Obstacle Detected"),
        ("DELIVERY_DELAY", "Delivery Delay"),
    ]

    SEVERITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]

    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name="alerts")
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts"
    )
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="LOW")
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alert_type} - {self.drone.drone_code}"
