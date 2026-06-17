from django.db import models

# Create your models here.
class Drone(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("MAINTENANCE", "Maintenance"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    model_name = models.CharField(max_length=100)
    #battery_level = models.IntegerField(default=100)
    drone_code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.model_name} ({self.drone_code}) - {self.status}"
