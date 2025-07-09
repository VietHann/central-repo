from rest_framework import routers
from .views import ProjectViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]