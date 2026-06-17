from django.db import models

# Create your models here.
from drones.models import Drone
class Delivery(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ASSIGNED", "Assigned"),
        ("IN_PROGRESS", "In Progress"),
        ("DELIVERED", "Delivered"),
        ("FAILED", "Failed"),
        ("CANCELLED", "Cancelled")
    ]
    delivery_code = models.CharField(max_length=50, unique=True)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name="deliveries")
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    assigned_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        #return f"Delivery to {self.drop_location} - {self.status}"
         return self.delivery_code