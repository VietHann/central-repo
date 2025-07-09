from rest_framework import generics
from .models import Crop
from .serializers import CropSerializer

class CropListCreate(generics.ListCreateAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

class CropRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer