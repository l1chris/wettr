import argparse
import logging
import sys

from weather_cli.display import (
    show_current_weather,
    show_daily_forecast,
    show_hourly_forecast,
)
from weather_cli.utils import get_location_from_ip
from weather_cli.weather import WeatherData, get_coordinates, get_current_weather


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

    if args.city:
        location = get_coordinates(args.city)
    else:
        location = get_location_from_ip()
        if not location:
            print("Could not auto-detect location.")
            city = input("Enter city name: ")
            location = get_coordinates(city)

    if not location:
        print("Error: Could not retrieve location data for city.")
        sys.exit(1)

    weather: WeatherData = get_current_weather(location["lat"], location["lon"])

    if not weather:
        print("Error: Could not retrieve weather data for location.")
        sys.exit(1)

    if args.f:
        show_current_weather(location, weather, True)
        show_hourly_forecast(weather, True)
        show_daily_forecast(weather, True)
    else:
        show_current_weather(location, weather)
        show_hourly_forecast(weather)
        show_daily_forecast(weather)


if __name__ == "__main__":
    main()
