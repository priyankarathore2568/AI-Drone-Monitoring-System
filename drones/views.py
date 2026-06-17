from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status


from .models import Drone
from .serializers import DroneSerializer

class DroneListView(APIView):
    def get(self, request):
        drones = Drone.objects.all()
        serializer = DroneSerializer(drones, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DroneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class DroneDetailView(APIView):
    def get(self, request, id):
        try:
            drone = Drone.objects.get(id=id)
        except Drone.DoesNotExist:
            return Response({"error": "Drone not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DroneSerializer(drone)
        return Response(serializer.data)
    
    def put(self, request, id):
        try:
            drone = Drone.objects.get(id=id)
        except Drone.DoesNotExist:
            return Response({"error": "Drone not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DroneSerializer(drone, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def delete(self, request, id):
        try:
            drone = Drone.objects.get(id=id)
        except Drone.DoesNotExist:
            return Response({"error": "Drone not found"}, status=status.HTTP_404_NOT_FOUND)

        drone.delete()
        return Response({"message": "Drone deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)