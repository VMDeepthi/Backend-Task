from django.http import JsonResponse
import requests
import os
import pycountry
from django.shortcuts import render


WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
LOCATION_API_KEY = os.getenv('LOCATION_API_KEY')

def get_weather(request):
   
    location_url = f'https://ipinfo.io/json?token={LOCATION_API_KEY}'
    location_response = requests.get(location_url)
    location_data = location_response.json()

   
    ip_address = location_data.get('ip', 'Unknown')
    city = location_data.get('city', 'Unknown')
    country_code = location_data.get('country', 'Unknown')

    
    try:
        country_name = pycountry.countries.get(alpha_2=country_code).name
    except AttributeError:
        country_name = country_code 

    
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

   
    if weather_response.status_code == 200:
       
        temperature_celsius = weather_data['main']['temp'] - 273.15
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']

       
        response = {
            'ip': ip_address,
            'location': {
                'city': city,
                'country': country_name
            },
            'weather': {
                'temperature': round(temperature_celsius, 2),  
                'humidity': humidity,
                'description': description
            }
        }
      
        return JsonResponse(response, json_dumps_params={'indent': 4, 'ensure_ascii': False})
    else:
        return JsonResponse({'error': 'Weather data not found or invalid API key.'}, status=400)

# def index(request):
#     return render(request, 'index.html')
