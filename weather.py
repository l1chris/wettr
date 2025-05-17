import requests

def get_coordinates(location):
  url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
  response = requests.get(url)
  data = response.json()
  first_result = data['results'][0]
  return first_result['latitude'], first_result['longitude']

def get_current_weather(lat, lon):
  url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
  response = requests.get(url)
  return response.json()['current_weather']
