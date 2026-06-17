from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Delivery
from .serializers import DeliverySerializer


class DeliveryListView(APIView):

    def get(self, request):
        deliveries = Delivery.objects.all()
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeliverySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryDetailView(APIView):

    def get(self, request, id):
        delivery = get_object_or_404(Delivery, id=id)
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)

    def put(self, request, id):
        delivery = get_object_or_404(Delivery, id=id)
        serializer = DeliverySerializer(delivery, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        delivery = get_object_or_404(Delivery, id=id)
        delivery.delete()
        return Response(
            {"message": "Delivery deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )