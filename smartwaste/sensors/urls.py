from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^data/$', views.receive_sensor_data, name='receive_sensor_data'),
]