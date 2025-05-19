from display import show_current_weather, show_daily_forecast, show_hourly_forecast
from utils import get_location_from_ip
from weather import get_current_weather


def main():
    location = get_location_from_ip()
    weather = get_current_weather(location["lat"], location["lon"])

    show_current_weather(location, weather)
    show_hourly_forecast(weather)
    show_daily_forecast(weather)


if __name__ == "__main__":
    main()
