from rest_framework import serializers
from .models import Drone

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        #fields = ['id', 'drone_code', 'model', 'status', 'battery_capacity']
        fields = "__all__"