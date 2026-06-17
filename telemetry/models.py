from django.db import models

# Create your models here.
from drones.models import Drone

class Telemetry(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name='telemetry_records')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    altitude = models.FloatField(default=0)
    speed = models.FloatField(default=0)
    battery_percentage = models.FloatField(default=0)
    
    network_signal_strength = models.IntegerField(default=0)

    direction = models.CharField(max_length=50,default="Unknown")

    area = models.CharField(max_length=100,default="Unknown")

    temperature = models.FloatField(default=0)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #return f"Telemetry for {self.drone} at {self.recorded_at}"
        return f"{self.drone.drone_code}  - {self.recorded_at}%"