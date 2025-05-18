from datetime import datetime

from rich import box, print
from rich.align import Align
from rich.panel import Panel
from rich.table import Table

from utils import get_ascii_title, get_icon, get_weekday


def show_current_weather(data):
    current = data["current_weather"]
    icon = get_icon(current["weathercode"])
    temp = current["temperature"]
    wind = current["windspeed"]

    ascii_title = get_ascii_title()
    ascii_block = Align(ascii_title, align="center", vertical="middle")

    table = Table.grid(expand=True)
    table.add_column(ratio=1)
    table.add_column(ratio=1)

    left_text = (
        f"\n"
        f"[bold]Weather in Oldenburg, Germany \n"
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
    table.add_column("Time", width=25)
    table.add_column("Temp", width=25)
    table.add_column("Weather", width=25, justify="center")

    for t, temp, code in zip(times, temps, codes):
        hour = t.split("T")[1][:5]
        table.add_row(hour, f"{temp}°C", get_icon(code))

    panel = Panel(table, title="[bold]Today[/bold]", title_align="left", width=80)

    print(panel)


def show_daily_forecast(data):
    days = data["daily"]["time"][:3]
    maxs = data["daily"]["temperature_2m_max"][:3]
    mins = data["daily"]["temperature_2m_min"][:3]
    codes = data["daily"]["weather_code"][:3]

    table = Table(width=75, box=box.MINIMAL)
    table.add_column("Day", width=25)
    table.add_column("Min/Max", width=25)
    table.add_column("Weather", width=25, justify="center")

    for d, tmin, tmax, code in zip(days, mins, maxs, codes):
        dt = datetime.fromisoformat(d)
        day = get_weekday(dt.weekday())
        table.add_row(day, f"{tmin}°C / {tmax}°C", get_icon(code))

    panel = Panel(table, title="[bold]Forecast[/bold]", title_align="left", width=80)

    print(panel)
