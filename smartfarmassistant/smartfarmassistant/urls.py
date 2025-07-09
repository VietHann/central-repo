from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('farms.urls')),
    path('api/', include('sensors.urls')),
    path('api/', include('iot.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]