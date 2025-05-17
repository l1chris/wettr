from weather import get_coordinates, get_current_weather
from utils import format_weather

def main():
  lat, lon = get_coordinates("Oldenburg")
  weather = get_current_weather(lat, lon)
  #print(weather)
  print(format_weather(weather,"Oldenburg"))

if __name__ == "__main__":
  main()