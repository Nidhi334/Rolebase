from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'doctor', DoctorViewSet)
router.register(r'testgroup', TestGroupViewSet)
router.register(r'test', TestViewSet)
router.register(r'package',PackageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]