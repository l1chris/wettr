from display import show_current_weather, show_daily_forecast, show_hourly_forecast
from weather import get_coordinates, get_current_weather


def main():
    lat, lon = get_coordinates("Oldenburg")
    weather = get_current_weather(lat, lon)

    show_current_weather(weather)
    show_hourly_forecast(weather)
    show_daily_forecast(weather)


if __name__ == "__main__":
    main()
