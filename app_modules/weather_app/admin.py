from django.contrib import admin
from .models import *

admin.site.register(Forecast)
admin.site.register(DayForecast)
admin.site.register(City)