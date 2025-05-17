from datetime import datetime
from rich import print
from rich.panel import Panel
from rich.table import Table
from utils import get_icon, get_weekday

def show_current_weather(data):
  current = data["current_weather"]
  icon = get_icon(current["weathercode"])
  temp = current["temperature"]
  wind = current["windspeed"]

  print(Panel(f"[bold]Now:[/bold]  {icon}  {temp}°C\n[bold]Wind:[/bold] {wind} km/h"))

def show_hourly_forecast(data):
  
  current_time = datetime.now()

  hourly_times = data['hourly']['time']

  index_before_now = -1

  for i in range(len(hourly_times)):
    time = datetime.fromisoformat(hourly_times[i])
    if time < current_time:
        index_before_now = i
    else:
        break  # since times are sorted, we can stop here

  times = data['hourly']['time'][index_before_now:index_before_now+8]
  temps = data['hourly']['temperature_2m'][index_before_now:index_before_now+8]
  codes = data['hourly']['weather_code'][index_before_now:index_before_now+8]

  table = Table(title="Today")
  table.add_column("Time")
  table.add_column("Temp")
  table.add_column("Weather")

  for t, temp, code in zip(times, temps, codes):
      hour = t.split("T")[1][:5]
      table.add_row(hour, f"{temp}°C", get_icon(code))

  print(table)

def show_daily_forecast(data):
  days = data['daily']['time'][:3]
  maxs = data['daily']['temperature_2m_max'][:3]
  mins = data['daily']['temperature_2m_min'][:3]
  codes = data['daily']['weather_code'][:3]

  table = Table(title="Forecast")
  table.add_column("Day")
  table.add_column("Min/Max")
  table.add_column("Weather")

  for d, tmin, tmax, code in zip(days, mins, maxs, codes):
      dt = datetime.fromisoformat(d)
      day = get_weekday(dt.weekday())
      table.add_row(day, f"{tmin}°C / {tmax}°C", get_icon(code))

  print(table)