
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'waves', views.WaveViewSet)
router.register(r'weather', views.WeatherViewSet)
router.register(r'tide', views.TideViewSet)
router.register(r'beach', views.BeachViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
