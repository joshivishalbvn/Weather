from django.urls import path
from .views import HomeView, LocationByCoordinatesView,UpdateWeatherDataView,WeatherDetailsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('location/', LocationByCoordinatesView.as_view(), name='location'),
    path('update-weather/', UpdateWeatherDataView.as_view(), name='update_weather'),
    path('details/<str:city>/<str:date>/hourly-weather-forecast/', WeatherDetailsView.as_view(), name='weather_Details'),
]
