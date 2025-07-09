from rest_framework import generics
from .models import Farm, Crop
from .serializers import FarmSerializer, CropSerializer

class FarmList(generics.ListCreateAPIView):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

class FarmDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

class CropList(generics.ListCreateAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

class CropDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer