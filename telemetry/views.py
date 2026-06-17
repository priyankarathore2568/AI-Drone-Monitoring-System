from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Telemetry
from .serializers import TelemetrySerializer

from alerts.models import Alert

class TelemetryListView(APIView):

    def get(self, request):
        telemetry_records = Telemetry.objects.all()
        serializer = TelemetrySerializer(telemetry_records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TelemetrySerializer(data=request.data)

        if serializer.is_valid():
            telemetry = serializer.save()

            if telemetry.battery_percentage < 20:
               Alert.objects.create(
                 drone=telemetry.drone,
                 alert_type="LOW_BATTERY",
                 severity="HIGH",
                 message="Battery dropped below 20%"
               )

            if telemetry.network_signal_strength < 30:
                Alert.objects.create(
                       drone=telemetry.drone,
                       alert_type="WEAK_SIGNAL",
                       severity="MEDIUM",
                       message="Network signal is weak"
                )

            if telemetry.temperature > 50:
                Alert.objects.create(
                  drone=telemetry.drone,
                  alert_type="HIGH_TEMPERATURE",
                  severity="CRITICAL",
                  message="Drone temperature is above safe limit"
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TelemetryDetailView(APIView):

    def get(self, request, id):
        telemetry = get_object_or_404(Telemetry, id=id)
        serializer = TelemetrySerializer(telemetry)
        return Response(serializer.data)
    
    def put(self, request, id):
        telemetry = get_object_or_404(Telemetry, id=id)
        serializer = TelemetrySerializer(telemetry, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        telemetry = get_object_or_404(Telemetry, id=id)
        telemetry.delete()
        return Response(
            {"message": "Telemetry deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )