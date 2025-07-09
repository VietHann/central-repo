from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.bin_list, name='bin_list'),
]