from rest_framework import generics
from .models import Sensor, SensorData
from .serializers import SensorSerializer, SensorDataSerializer

class SensorList(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SensorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SensorDataList(generics.ListCreateAPIView):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

class SensorDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer