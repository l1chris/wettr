from datetime import datetime
from zoneinfo import ZoneInfo

from rich import box, print
from rich.align import Align
from rich.panel import Panel
from rich.table import Table

from utils import get_ascii_title, get_icon, get_weekday, to_fahrenheit


def show_current_weather(location_data, weather_data, in_fahrenheit=False):
    current = weather_data["current_weather"]
    icon = get_icon(current["weathercode"])
    temp = current["temperature"]
    wind = current["windspeed"]

    tzinfo = ZoneInfo(weather_data["timezone"])
    current_time = datetime.now(tz=tzinfo)
    formatted_time = current_time.strftime("%H:%M")

    ascii_title = get_ascii_title()
    ascii_block = Align(ascii_title, align="center", vertical="middle")

    table = Table.grid(expand=True)
    table.add_column(ratio=1)
    table.add_column(ratio=1)

    city = location_data["city"]
    country = location_data["country"]

    temp_converted = f"{to_fahrenheit(temp)}°F" if in_fahrenheit else f"{temp}°C"

    left_text = (
        f"\n"
        f"[bold]{city}, {country} \n"
        f"\n"
        f"Now:[bold]  {icon}  {temp_converted} \n"
        f"Wind:[bold] {wind} km/h \n"
        f"Local time: {formatted_time}"
    )

    table.add_row(left_text, ascii_block)

    panel = Panel(
        table,
        # title="[bold blue]Current Weather[/bold blue]",
        title="[bold]Current Weather[/bold]",
        # border_style="blue",
        title_align="left",
        width=80,
    )
    print(panel)


def show_hourly_forecast(weather_data, in_fahrenheit=False):
    tzinfo = ZoneInfo(weather_data["timezone"])
    current_time = datetime.now(tz=tzinfo)

    curr = current_time.hour
    last = curr + 9

    # Get every 2nd entry starting from the current time
    times = weather_data["hourly"]["time"][curr:last:2]
    temps = weather_data["hourly"]["temperature_2m"][curr:last:2]
    codes = weather_data["hourly"]["weather_code"][curr:last:2]

    table = Table(width=75, box=box.MINIMAL)

    for time in times:
        hour = time.split("T")[1][:5]
        table.add_column(hour, justify="center")

    icons = [get_icon(code) for code in codes]
    temps_converted = [
        f"{to_fahrenheit(temp)}°F" if in_fahrenheit else f"{temp}°C" for temp in temps
    ]

    table.add_row(*icons)
    table.add_row(*temps_converted)

    panel = Panel(table, title="[bold]Today[/bold]", title_align="left", width=80)

    print(panel)


def show_daily_forecast(weather_data, in_fahrenheit=False):
    days = weather_data["daily"]["time"][1:4]
    maxs = weather_data["daily"]["temperature_2m_max"][1:4]
    mins = weather_data["daily"]["temperature_2m_min"][1:4]
    codes = weather_data["daily"]["weather_code"][1:4]

    weekdays = [get_weekday(datetime.fromisoformat(d).weekday()) for d in days]

    table = Table(width=75, box=box.MINIMAL)

    for weekday in weekdays:
        table.add_column(weekday, width=25, justify="center")

    icons = [get_icon(code) for code in codes]
    maxs_converted = [
        f"{to_fahrenheit(max)}°F" if in_fahrenheit else f"{max}°C" for max in maxs
    ]
    mins_converted = [
        f"{to_fahrenheit(min)}°F" if in_fahrenheit else f"{min}°C" for min in mins
    ]
    temps = [f"{tmin} / {tmax}" for tmin, tmax in zip(mins_converted, maxs_converted)]

    table.add_row(*icons)
    table.add_row(*temps)

    panel = Panel(table, title="[bold]Forecast[/bold]", title_align="left", width=80)

    print(panel)
