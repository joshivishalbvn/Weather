from django.urls import path
from .consumers import WeatherConsumer

websocket_urlpatterns = [
    path('ws/data/<str:city>/', WeatherConsumer.as_asgi()),
]
