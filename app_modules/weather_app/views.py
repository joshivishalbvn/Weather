import json
import datetime
from .models import City
from .forms import CityForm
from django.views import View
from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView 
from app_modules.weather_app.utils import (
    get_7_day_forecast, 
    get_hourly_data_by_date, 
    get_location_from_coordinates,
    get_coordinates_from_city_name,
)

class HomeView(TemplateView):
    
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx =  super().get_context_data(**kwargs)
        today = datetime.datetime.today()
        ctx["form"] = CityForm
        ctx["cities"] = City.objects.all()
        ctx["today_name"] = today.strftime('%A')
        ctx["formatted_date"] = today.strftime("%d %b")
        return ctx

class LocationByCoordinatesView(View):
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        weather_data = {}
        weather_data["weather_data"] = get_7_day_forecast(data.get('latitude'), data.get('longitude'))
        weather_data["location_info"] = get_location_from_coordinates(data.get('latitude'), data.get('longitude'))
        return JsonResponse(weather_data)

class UpdateWeatherDataView(View):

    def post(self,request):
        form = CityForm(request.POST)
        if form.is_valid():
            latitude,longitude = get_coordinates_from_city_name(form.cleaned_data['city'])
            data = {}
            data["weather_data"] = get_7_day_forecast(latitude, longitude)
            data["location_info"] = get_location_from_coordinates(latitude, longitude)
            return JsonResponse(data)

class WeatherDetailsView(View):

    def get(self, request, city, date):
        
        latitude, longitude = get_coordinates_from_city_name(city)
        
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        previous_date = date_obj - datetime.timedelta(days=1)
        next_date = date_obj + datetime.timedelta(days=1)
        day_of_week = date_obj.strftime("%A")
        
        context = {
            'date': date,
            'city_name': city,
            'date_obj': date_obj,
            'day_of_week': day_of_week,
            'hourly_data': get_hourly_data_by_date(latitude, longitude, date),
        }
        
        today = datetime.datetime.today().date()
        last_day_of_week = today + datetime.timedelta(days=7)
        
        if previous_date.date() >= today:
            context['previous_date'] = previous_date.strftime('%d-%m-%Y')
            context["previous_date_url"] = reverse('weather_Details', kwargs={'city': city, 'date': previous_date.strftime('%Y-%m-%d')})
        
        if next_date.date() < last_day_of_week:
            context['next_date'] = next_date.strftime('%d-%m-%Y')
            context["next_date_url"] = reverse('weather_Details', kwargs={'city': city, 'date': next_date.strftime('%Y-%m-%d')})
        
        return render(request, 'details.html', context)