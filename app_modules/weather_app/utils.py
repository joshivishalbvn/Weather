import pytz
import requests
from datetime import datetime
from django.conf import settings

def get_location_from_coordinates(latitude,longitude):

    url = f'https://api.geoapify.com/v1/geocode/reverse?lat={latitude}&lon={longitude}&apiKey={settings.GEO_APIFY_API_KEY}'

    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Unable to get location data, status code: {response.status_code}"}
    
    data = response.json()

    if 'features' in data and len(data['features']) > 0:
        location = data['features'][0]['properties']['formatted']  
        city = data['features'][0]['properties'].get('city', 'Unknown City')
        country = data['features'][0]['properties'].get('country', 'Unknown Country')
        data = {"location": location, "city": city, "country": country}
        return data
    else:
        return {"error": "No location found for these coordinates"}
    
def get_coordinates_from_city_name(city_name):

    url = f'https://api.geoapify.com/v1/geocode/search?text={city_name}&apiKey={settings.GEO_APIFY_API_KEY}'

    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Unable to get location data, status code: {response.status_code}"}
    
    data = response.json()
    
    if 'features' in data and len(data['features']) > 0:
        lat = data['features'][0]['geometry']['coordinates'][1]  
        lon = data['features'][0]['geometry']['coordinates'][0] 
        return lat,lon
    else:
        return {"error": "No location found for the city"} 

def get_7_day_forecast(latitude,longitude):

    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,wind_direction_10m_dominant&timezone=Asia/Kolkata'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        forecast = data['daily']
        weather_data = []
        for i in range(len(forecast['temperature_2m_max'])):
            date_string = forecast['time'][i]  
            date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
            day_name = date_object.strftime('%A') 
            day_forecast = {
                "day": i,
                "date": forecast['time'][i],
                "day_name":day_name,
                "max_temp": forecast['temperature_2m_max'][i],
                "min_temp": forecast['temperature_2m_min'][i],
                "precipitation": forecast['precipitation_sum'][i],
                "windspeed_max": forecast['windspeed_10m_max'][i],
                "wind_direction": forecast['wind_direction_10m_dominant'][i]
            }
            weather_data.append(day_forecast)
        
        return weather_data
    else:
        return {"error": f"Unable to fetch forecast data. Status code: {response.status_code}"}
    
def get_hourly_data_by_date(latitude,longitude,date):
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone=Asia/Kolkata&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,wind_gusts_10m,weather_code,cloud_cover,visibility'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return filter_current_and_upcoming_data(data["hourly"],date)
    
    else:
        return {"error": f"Unable to fetch forecast data. Status code: {response.status_code}"}
    
    
weatherCodes = {
    0: 'Mostly sunny',      
    1: 'Mainly Clear',      
    2: 'Cloudy',     
    3: 'Light Rain',           
    4: 'Heavy Rain',            
    5: 'Showers',            
    6: 'Thunderstorms',   
    7: 'Snow',          
    8: 'Sleet',           
    9: 'Windy',          
    10: 'Fog', 
    11: 'Mist',       
    12: 'Tropical Storm',        
    13: 'Clear with Clouds', 
    14: 'Misty',           
    15: 'Tropical Storm',  
}

def filter_current_and_upcoming_data(hourly_data, date):
    current_and_upcoming_data = {
        "time": [],
        "temperature_2m": [],
        "relative_humidity_2m": [],
        "dew_point_2m": [],
        "wind_gusts_10m": [],
        "weather_code": [],
        "weather_description": [] ,
        "visibility": [] ,
        "cloud_cover": [] 
    }

    kolkata_tz = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(kolkata_tz)  
    current_hour = current_time.strftime("%H")  
    today_date = current_time.strftime("%Y-%m-%d")

    is_today = date == today_date
    
    for i, time in enumerate(hourly_data["time"]):
        if time.startswith(date):  
            time_hour = time[11:13]  
            if is_today and time_hour >= current_hour or not is_today:
                current_and_upcoming_data["time"].append(time[11:16])  
                current_and_upcoming_data["temperature_2m"].append(hourly_data["temperature_2m"][i])
                current_and_upcoming_data["relative_humidity_2m"].append(hourly_data["relative_humidity_2m"][i])
                current_and_upcoming_data["dew_point_2m"].append(hourly_data["dew_point_2m"][i])
                current_and_upcoming_data["wind_gusts_10m"].append(hourly_data["wind_gusts_10m"][i])
                current_and_upcoming_data["cloud_cover"].append(hourly_data["cloud_cover"][i])
                visibility_km = hourly_data["visibility"][i] / 1000
                current_and_upcoming_data["visibility"].append(visibility_km)
                weather_code = hourly_data["weather_code"][i]
                current_and_upcoming_data["weather_code"].append(weather_code)
                current_and_upcoming_data["weather_description"].append(weatherCodes.get(weather_code, 'Unknown Weather'))
    
    return current_and_upcoming_data