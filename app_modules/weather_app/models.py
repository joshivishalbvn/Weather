from django.db import models

class Forecast(models.Model):
    
    city      = models.CharField(max_length=100)
    country   = models.CharField(max_length=100,null=True,blank=True)
    latitude  = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Forecast for {self.city}, {self.country}"

class DayForecast(models.Model):

    created_at     = models.DateTimeField(auto_now_add=True,null=True)
    forecast       = models.ForeignKey(Forecast, on_delete=models.CASCADE, related_name='day_forecasts', blank=True, null=True)
    date           = models.DateField()
    day_name       = models.CharField(max_length=20)
    max_temp       = models.FloatField()
    min_temp       = models.FloatField()
    precipitation  = models.FloatField()
    windspeed_max  = models.FloatField()
    wind_direction = models.CharField(max_length=20)

    def __str__(self):
        return f"Forecast for {self.day_name} ({self.date})"
    

class City(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name