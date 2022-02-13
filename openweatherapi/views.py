from django.shortcuts import render
import requests
from django.conf import settings


def openweather(request):
    
    data = {}

    if request.method == 'POST':
        # Get the user input
        city = request.POST['city']
        # The API Key
        openweather_api_key = settings.OPENWEATHER_API_KEY

        # The API endpoint
        api = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&appid=' + openweather_api_key
        
        # Convert the response into a python dictionary
        retrieved_data = requests.get(api).json()
        
        try:
            # Manipulate the data
            data = {
                "city": str(retrieved_data['name']),
                "country_code": str(retrieved_data['sys']['country']),
                "latitude": str(retrieved_data['coord']['lat']) + '°',
                "longitude": str(retrieved_data['coord']['lon']) + '°',
                "temp": str(round(retrieved_data['main']['temp'])) + ' °C',
                "pressure": str(retrieved_data['main']['pressure']) + " hPa",
                "humidity": str(retrieved_data['main']['humidity']) + '%',
                'main': str(retrieved_data['weather'][0]['main']),
                'description': str(retrieved_data['weather'][0]['description']),
                'icon': retrieved_data['weather'][0]['icon'],
            }

        except KeyError:
            # If the city is not found, display the errors below
            data = {
                "error_line_1": "Whoops... Something went wrong...",
                "error_line_2": "Please make sure that the name of the city you entered is in English and it's spelled correctly.",
            }

    return render(request, "openweatherapi/openweatherapi.html", data)

