from rest_framework import generics
from .models import WeatherData
from .serializers import WeatherDataSerializer

class WeatherDataListCreate(generics.ListCreateAPIView):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer

class WeatherDataRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer