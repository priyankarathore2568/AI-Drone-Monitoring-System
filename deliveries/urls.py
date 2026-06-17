from django.urls import path
from .views import DeliveryListView, DeliveryDetailView


urlpatterns = [
    path("deliveries/", DeliveryListView.as_view(), name="delivery-list"),
    path("deliveries/<int:id>/", DeliveryDetailView.as_view(), name="delivery-detail"),
]