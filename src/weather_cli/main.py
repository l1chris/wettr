import argparse
import logging
import sys

from weather_cli.display import (
    show_current_weather,
    show_daily_forecast,
    show_hourly_forecast,
)
from weather_cli.utils import Geodata, get_coordinates_for_ip
from weather_cli.weather import (
    WeatherData,
    get_coordinates_for_city,
    get_current_weather,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Weather CLI")
    parser.add_argument("--city", type=str, help="City to get weather for")
    parser.add_argument(
        "--f", action="store_true", help="Display temperature in Fahrenheit"
    )
    return parser.parse_args()


def main():
    logging.basicConfig(filename="main.log")
    args = parse_args()

    coordinates: Geodata

    if args.city:
        coordinates = get_coordinates_for_city(args.city)
    else:
        coordinates = get_coordinates_for_ip()
        if not coordinates:
            print("Could not auto-detect location.")
            city = input("Enter city name: ")
            coordinates = get_coordinates_for_city(city)

    if not coordinates:
        print("Error: Could not retrieve coordinates for city.")
        sys.exit(1)

    weather: WeatherData = get_current_weather(coordinates.lat, coordinates.lon)

    if not weather:
        print("Error: Could not retrieve weather data for location.")
        sys.exit(1)

    if args.f:
        show_current_weather(coordinates, weather, True)
        show_hourly_forecast(weather, True)
        show_daily_forecast(weather, True)
    else:
        show_current_weather(coordinates, weather)
        show_hourly_forecast(weather)
        show_daily_forecast(weather)


if __name__ == "__main__":
    main()
