import requests
from django.shortcuts import render

def home(request):
    weather_data = None
    error_message = None

    if 'city' in request.GET:
        city = request.GET['city']

        # Step 1: Convert City Name to Latitude & Longitude
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_response = requests.get(geo_url)

        if geo_response.status_code == 200 and geo_response.json().get("results"):
            geo_data = geo_response.json()["results"][0]
            latitude, longitude = geo_data["latitude"], geo_data["longitude"]

            # Step 2: Fetch Weather Data from Open-Meteo
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
            weather_response = requests.get(weather_url)

            if weather_response.status_code == 200:
                weather_json = weather_response.json()
                current_weather = weather_json["current"]

                weather_data = {
                    "city": geo_data["name"],
                    "temperature": current_weather["temperature_2m"],
                    "wind_speed": current_weather["wind_speed_10m"],
                    "humidity": weather_json["hourly"]["relative_humidity_2m"][0]  # Get the first hour's humidity
                }
            else:
                error_message = "Could not fetch weather data. Please try again."
        else:
            error_message = "City not found. Please check the spelling and try again."

    return render(request, "weather/home.html", {"weather": weather_data, "error": error_message})
