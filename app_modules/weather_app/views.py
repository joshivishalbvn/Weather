import json
import datetime
from .models import City
from .forms import CityForm
from django.urls import reverse
from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
from django.views.generic import TemplateView ,View
from app_modules.weather_app.utils import (
    get_hourly_data_by_date, 
    get_weather_and_location,
    get_coordinates_from_city_name,
)

class HomeView(TemplateView):
    
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # cache.clear()
        ctx =  super().get_context_data(**kwargs)
        selected_city = self.request.session.get('selected_city', None)
        today = datetime.datetime.today()
        city_obj = City.objects.filter(name=selected_city).last()
        ctx["form"] = CityForm(initial={'city': city_obj})
        ctx["cities"] = City.objects.all()
        ctx["today_name"] = today.strftime('%A')
        ctx["formatted_date"] = today.strftime("%d %b")
        return ctx

class UpdateWeatherDataView(View):

    def post(self, request):
        form = CityForm(request.POST)
        
        if form.is_valid():
            try:
                city_name = form.cleaned_data['city'].name
                request.session['selected_city'] = city_name

                latitude, longitude = get_coordinates_from_city_name(city_name)

                weather_data, location_info = get_weather_and_location(latitude, longitude,timeout=12)

                data = {
                    "weather_data": weather_data,
                    "location_info": location_info
                }
                return JsonResponse(data)
            except Exception as e:
                print('\033[91m'+'e: ' + '\033[92m', e)
                pass
           
        else:
            return JsonResponse({"error": "Invalid form data"}, status=400)
        
class LocationByCoordinatesView(View):
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        city = self.request.session.get('selected_city', None)

        if city:
            latitude, longitude = get_coordinates_from_city_name(city)

        weather_data, location_info = get_weather_and_location(latitude, longitude,timeout=30)

        response_data = {
            "weather_data": weather_data,
            "location_info": location_info
        }

        return JsonResponse(response_data)

class WeatherDetailsView(View):

    def get(self, request, city, date):
        # cache.clear()
        cache_key = f"weather_data_{city}_{date}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return render(request, 'details.html', cached_data)
        
        latitude, longitude = get_coordinates_from_city_name(city)
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        today_date = datetime.datetime.today().date()
        request.session['selected_city'] = city 
         
        week_day_data = {}

        for i in range(7):
            day = today_date + datetime.timedelta(days=i)
            week_day_data[day.strftime("%A")] = {
                "date": day.strftime("%Y-%m-%d"),
                "is_current_day": day == date_obj.date(),
                "url": reverse('weather_Details', kwargs={'city': city, 'date': day.strftime('%Y-%m-%d')})
            }
            
        day_of_week = date_obj.strftime("%A")
        
        context = {
            'date': date,
            'city_name': city,
            'date_obj': date_obj,
            'day_of_week': day_of_week,
            'week_data': week_day_data,
            'hourly_data': get_hourly_data_by_date(latitude, longitude, date),
        }
        cache.set(cache_key, context, timeout=12 * 60 * 60)
        return render(request, 'details.html', context)