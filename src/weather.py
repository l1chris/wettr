import requests


def get_coordinates(location):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
    response = requests.get(url)
    data = response.json()
    first_result = data["results"][0]
    return first_result["latitude"], first_result["longitude"], first_result["country"]


def get_current_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=temperature_2m,weather_code"
        f"&daily=temperature_2m_max,temperature_2m_min,weather_code"
        f"&forecast_days=4"
        f"&timezone=auto"
    )
    response = requests.get(url)
    return response.json()
