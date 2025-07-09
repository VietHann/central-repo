from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/crops/', include('crops.urls')),
    path('api/weather/', include('weather.urls')),
    path('api/iot/', include('iot.urls')),
]