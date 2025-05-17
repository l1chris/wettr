def format_weather(data, location):
  return (
      f"Weather for {location}:\n"
      f"  Temperature: {data['temperature']}°C\n"
      f"  Wind Speed: {data['windspeed']} km/h\n"
      f"  Time: {data['time']}"
  )