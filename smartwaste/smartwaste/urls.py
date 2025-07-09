from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bins/', include('bins.urls')),
    url(r'^routes/', include('routes.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^sensors/', include('sensors.urls')),
)