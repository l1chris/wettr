from datetime import datetime

from rich import box, print
from rich.align import Align
from rich.panel import Panel
from rich.table import Table

from utils import get_ascii_title, get_icon, get_weekday


def show_current_weather(location_data, weather_data):
    current = weather_data["current_weather"]
    icon = get_icon(current["weathercode"])
    temp = current["temperature"]
    wind = current["windspeed"]

    ascii_title = get_ascii_title()
    ascii_block = Align(ascii_title, align="center", vertical="middle")

    table = Table.grid(expand=True)
    table.add_column(ratio=1)
    table.add_column(ratio=1)

    city = location_data["city"]
    country = location_data["country"]

    left_text = (
        f"\n"
        f"[bold]{city}, {country} \n"
        f"\n"
        f"Now:[bold]  {icon}  {temp}°C \n"
        f"Wind:[bold] {wind} km/h"
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


def show_hourly_forecast(data):

    current_time = datetime.now()

    hourly_times = data["hourly"]["time"]

    index_before_now = -1

    for i in range(len(hourly_times)):
        time = datetime.fromisoformat(hourly_times[i])
        if time < current_time:
            index_before_now = i
        else:
            break  # since times are sorted, we can stop here

    times = data["hourly"]["time"][index_before_now : index_before_now + 8]
    temps = data["hourly"]["temperature_2m"][index_before_now : index_before_now + 8]
    codes = data["hourly"]["weather_code"][index_before_now : index_before_now + 8]

    table = Table(width=75, box=box.MINIMAL)

    for time in times:
        hour = time.split("T")[1][:5]
        table.add_column(hour, justify="center")

    icons = [get_icon(code) for code in codes]
    temps = [f"{temp}°C" for temp in temps]

    table.add_row(*icons)
    table.add_row(*temps)

    panel = Panel(table, title="[bold]Today[/bold]", title_align="left", width=80)

    print(panel)


def show_daily_forecast(data):
    days = data["daily"]["time"][1:4]
    maxs = data["daily"]["temperature_2m_max"][1:4]
    mins = data["daily"]["temperature_2m_min"][1:4]
    codes = data["daily"]["weather_code"][1:4]

    weekdays = [get_weekday(datetime.fromisoformat(d).weekday()) for d in days]

    table = Table(width=75, box=box.MINIMAL)

    for weekday in weekdays:
        table.add_column(weekday, width=25, justify="center")

    icons = [get_icon(code) for code in codes]
    temps = [f"{tmin}°C / {tmax}°C" for tmin, tmax in zip(mins, maxs)]

    table.add_row(*icons)
    table.add_row(*temps)

    panel = Panel(table, title="[bold]Forecast[/bold]", title_align="left", width=80)

    print(panel)
