from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('farms/', include('farms.urls')),
    path('sensors/', include('sensors.urls')),
    path('irrigation/', include('irrigation.urls')),
    path('reports/', include('reports.urls')),
]