from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.route_list, name='route_list'),
]