import argparse

from weather_cli.display import (
    show_current_weather,
    show_daily_forecast,
    show_hourly_forecast,
)
from weather_cli.utils import get_location_from_ip
from weather_cli.weather import get_coordinates, get_current_weather


def parse_args():
    parser = argparse.ArgumentParser(description="Weather CLI")
    parser.add_argument("--city", type=str, help="City to get weather for")
    parser.add_argument(
        "--f", action="store_true", help="Display temperature in Fahrenheit"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.city:
        lat, lon, country = get_coordinates(args.city)
        location = {"city": args.city, "country": country, "lat": lat, "lon": lon}
    else:
        location = get_location_from_ip()

    weather = get_current_weather(location["lat"], location["lon"])

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
