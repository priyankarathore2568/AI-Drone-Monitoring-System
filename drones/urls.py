from django.urls import path
#from.views import DroneListCreateView, DroneRetrieveUpdateDestroyView
from .views import DroneListView, DroneDetailView


urlpatterns = [    path('drones/', DroneListView.as_view(), name='drone-list'),
    path('drones/<int:id>/', DroneDetailView.as_view(), name='drone-detail'),
]
