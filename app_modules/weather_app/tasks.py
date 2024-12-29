import asyncio
import random
from .models import City
from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Forecast, DayForecast
from channels.layers import get_channel_layer
from app_modules.weather_app.utils import get_7_day_forecast

@shared_task
def get_weather_data():
    all_cities = City.objects.values_list("name",flat=True)
    for city in all_cities:
        print('\033[91m'+'city: ' + '\033[92m', city)
        forecast, created = Forecast.objects.get_or_create(
            city=city,
            latitude=22.9965824,  
            longitude=72.6007808  
        )
        if created:
            print(f"New forecast entry created for {city}")
        else:
            print(f"Found existing forecast for {city}")

        try:
            current_time = timezone.now()

            existing_obj = DayForecast.objects.filter(
                forecast=forecast,
                created_at__gte=current_time - timedelta(seconds=30) 
            ).first()

            if existing_obj:
                print("Entry already exists within the last 5 minutes. Skipping.")
            else:
                data = get_7_day_forecast(22.9965824, 72.6007808)
                print('\033[91m' + 'data: ' + '\033[92m', data[0])
                day_data = data[0]
                day_date = datetime.strptime(day_data['date'], '%Y-%m-%d').date()  
                day_name = day_data['day_name']
                max_temp = day_data['max_temp']
                min_temp = day_data['min_temp']
                precipitation = day_data['precipitation']
                windspeed_max = day_data['windspeed_max']
                wind_direction = day_data['wind_direction']
                new_obj = DayForecast.objects.create(
                    forecast=forecast,
                    date=day_date,
                    day_name=day_name,
                    max_temp=max_temp,
                    min_temp=min_temp,
                    precipitation=precipitation,
                    windspeed_max=windspeed_max,
                    wind_direction=wind_direction
                )
                data = {}
                # data["temperature"] = max_temp
                data["temperature"] = random.randint(0, 100)
                data["wind_speed"] = windspeed_max
                data["wind_direction"] = wind_direction
                print('\033[91m'+'location["city"]: ' + '\033[92m', city)
                broadcast_websocket_message.delay(
                    group_name="CITY_{}".format(city),
                    payload=data
                )
                print(f"Saved forecast for {day_data['day_name']} ({day_data['date']})")
        except Exception as e:
            print('\033[91m'+'e: ' + '\033[92m', e)

async def broadcast_websocket_message_async(payload,group_name):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(group_name,{"type":"broadcast_message","message":payload})

@shared_task()
def broadcast_websocket_message(payload,group_name):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(broadcast_websocket_message_async(payload,group_name))
    loop.close()