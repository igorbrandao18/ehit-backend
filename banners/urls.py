from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'banners', BannerViewSet, basename='banner')

urlpatterns = router.urls

