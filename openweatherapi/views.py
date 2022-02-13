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
        list_of_data = requests.get(api).json()
        
        try:
            # Manipulate the data
            data = {
                "country_code": str(list_of_data['sys']['country']),
                "latitude": str(list_of_data['coord']['lat']) + '°',
                "longitude": str(list_of_data['coord']['lon']) + '°',
                "temp": str(list_of_data['main']['temp']) + ' °C',
                "pressure": str(list_of_data['main']['pressure']) + " hPa",
                "humidity": str(list_of_data['main']['humidity']) + '%',
                'main': str(list_of_data['weather'][0]['main']),
                'description': str(list_of_data['weather'][0]['description']),
                'icon': list_of_data['weather'][0]['icon'],
            }
        except KeyError:
            # If the city is not found, display the errors below
            data = {
                "error_line_1": "Whoops... Something went wrong...",
                "error_line_2": "Please make sure that the name of the city you entered is in English and it's spelled correctly.",
            }

    return render(request, "openweatherapi/openweatherapi.html", data)

