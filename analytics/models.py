from django.db import models

# Create your models here.

from drones.models import Drone


class Detection(models.Model):

    OBJECT_TYPES = [
        ("PERSON", "Person"),
        ("CAR", "Car"),
        ("TRUCK", "Truck"),
        ("BUS", "Bus"),
        ("MOTORBIKE", "Motorbike"),
    ]

    RISK_LEVELS = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]

    drone = models.ForeignKey(
        Drone,
        on_delete=models.CASCADE
    )

    object_type = models.CharField(
        max_length=30,
        choices=OBJECT_TYPES
    )

    confidence = models.FloatField()

    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVELS
    )

    image_path = models.CharField(
        max_length=300
    )

    detected_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.object_type} - {self.risk_level}"